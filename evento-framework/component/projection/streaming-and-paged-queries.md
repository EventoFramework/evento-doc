---
description: Large query answers without filling the Evento Server's memory
---

# Streamed and Paged Queries

A classic query answer travels as **one message**: the projection builds the whole `Multiple<View>`, the Evento Server receives it whole and forwards it whole, and the caller holds it whole before it can read the first view. For a few kilobytes that is the right trade-off; for an export of hundreds of megabytes it means the whole result sits in the memory of three processes at once, the server among them.

Since Evento **3.0** queries have three more options, which can be combined:

* **Streamed queries** — the caller pulls the views as it consumes them, with flow control end to end: no hop ever holds more than a small window of the result.
* **Direct streams** — the views travel from the answering bundle to the caller on a direct connection, and never cross the Evento Server.
* **Pages** — a `Page<View>` answer for results the caller wants one slice at a time.

Existing query handlers and callers keep working unchanged.

## Streaming a query

Any query can be streamed by the caller with `QueryGateway.stream(...)`. It returns a `QueryStream<V>`, an `Iterable<V>` that must be closed (try-with-resources):

```java
try (var orders = queryGateway.stream(new ExportOrdersQuery(customerId))) {
    for (OrderView order : orders) {
        writer.write(order);            // views arrive while the rest is still travelling
    }
}

// or as a java.util.stream.Stream
try (var orders = queryGateway.stream(new ExportOrdersQuery(customerId))) {
    orders.stream().filter(OrderView::isOpen).forEach(this::process);
}
```

This works for **every query handler, whatever it answers with**: a `Multiple` is sent in frames, a `Single` is a stream of one view. The views are sent in frames of about 256 KiB, and only as many frames as the caller's **window** may be in flight (default 16): the answering bundle sends a frame only when the caller has granted credit for it, and the caller grants credit as it consumes. A slow consumer slows the producer down instead of piling the result up in the server.

Options go through `QueryOptions`:

```java
queryGateway.stream(query, QueryOptions.defaults()
        .window(32)                         // frames in flight ahead of the consumer
        .timeout(Duration.ofSeconds(30))    // longest wait for the next frame
        .direct());                         // see Direct streams
```

* The **timeout** of a stream bounds each wait for the next frame, not the whole stream: a long export that keeps flowing does not time out.
* **Closing** the stream early (leaving the `for`, an exception), the caller disconnecting, the answering bundle disconnecting, or a caller that stops granting credit for the timeout: each ends the stream on both sides and closes the handler's source.
* A failure of the handler while streaming surfaces as a `QueryStream.QueryStreamException` thrown by the iteration.
* A handler that cannot stream (a bundle older than 3.0, or a session through a 2.5 server) answers whole, and the stream simply iterates that answer: callers can adopt `stream` before every bundle is upgraded.

## Producing lazily: `Streamed<View>`

Streaming the answer of a `Multiple` already spares the server and the caller, but the projection still builds the whole list. To produce views only as fast as the caller consumes them, return a `Streamed` built on a **source that is not opened yet**:

```java
@QueryHandler
Streamed<OrderView> handle(ExportOrdersQuery query) {
    return Streamed.of(() -> repository.streamByCustomer(query.getCustomerId())); // a DB cursor
}
```

* Asked with `stream`, the framework opens the source, reads it as frames are sent, and closes it at the end, on cancel or on failure.
* Asked with the plain `query`, the views are collected and sent in one reply, as a `Multiple` would be: the query keeps working for callers that do not stream, at a `Multiple`'s cost. Declare the query as `Query<Streamed<OrderView>>`.

{% hint style="warning" %}
The source is opened **after** the query handler has returned, outside any interceptor around it. A source that needs a transaction or a connection (a JPA or JDBC stream) must open and close it itself, inside the supplier and in the stream's `onClose`.
{% endhint %}

`Streamed.of(Iterable)` wraps views already in memory.

## Direct streams (bundle to bundle)

With a stream through the server, the server relays frames as it reads them and keeps nothing but the forwarding entry — but every byte still crosses it. For very large results the answering bundle can offer its streams on its **own endpoint**:

<pre class="language-java"><code class="lang-java">EventoBundle.Builder.builder()
...
<strong>.setDirectStreamConfig(DirectStreamConfig.on(3040, "orders-query.internal"))
</strong>...
</code></pre>

and a caller asks for it with `QueryOptions.defaults().direct()`. The server still routes the query (choice of the instance, authorization, tracing), then relays a single redirect carrying a random, **single-use ticket** bound to that stream (valid 10 seconds). The caller connects to the endpoint, presents the ticket, and the data never touches the server.

If the endpoint cannot be reached, TLS does not match, or the ticket is refused or expired, the caller **asks the stream again through the server on its own**: the option can be turned on without knowing every caller's network. `DirectStreamConfig` also offers `withTls(sslContext)`, `withAdvertisedPort(port)` (NAT, port mapping) and `withTicketTtl(duration)`. The counters `BundleClient.directStreamsServed()`, `directStreamsFollowed()` and `directStreamFallbacks()` tell how often the direct path was taken.

## Paged answers: `Page<View>` and `PageRequest`

When the caller wants a slice rather than everything, answer with a `Page`. The query carries a `PageRequest`:

```java
public class ListOrdersQuery extends Query<Page<OrderView>> {
    private String customerId;
    private PageRequest page;
    // constructors, getters, setters
}

@QueryHandler
Page<OrderView> handle(ListOrdersQuery query) {
    var request = query.getPage();
    var views = repository.find(query.getCustomerId(), request.offset(), request.getSize());
    return Page.of(views, request.getNumber(), request.getSize(), repository.count(query.getCustomerId()));
}
```

* **Offset pages**: `PageRequest.first(size)`, `PageRequest.of(number, size)`; `Page.of(items, number, size, totalElements)` (pass `-1` when the total is unknown or too expensive). `getTotalPages()` is derived from it.
* **Cursor pages** (stable under concurrent inserts, cheap on large tables): `PageRequest.after(cursor, size)` and `Page.ofCursor(items, nextCursor)`.
* `page.hasNext()` and `page.next()` give the `PageRequest` of the following page, whatever the kind.

A `Page` can be streamed too: `stream` iterates its items.

## Answered in the same bundle

A bundle that both asks and handles a query answers it **itself**, without the server (`EventoBundle.Builder.setLocalQueryShortCircuit`, default `true`). The query still takes exactly the path of a remote one — serialization, interceptors, `TracingAgent`, performance metrics — so tracing and the GUI dashboards see it as before, and a view that does not serialize fails locally too. Streams short-circuit the same way. Commands always go through the server. A bundle not yet enabled (projectors still catching up) does not serve itself.

## Compression

Answers of 32 KiB or more are compressed end to end (DEFLATE) when that saves at least an eighth; the server relays the compressed bytes untouched. Tune it with `setCompressionThreshold(bytes)` and `setAcceptCompressedReplies(boolean)` on the bundle builder.

## Why: what an answer costs the server

Since 3.0 the server does not keep query answers at all (queries are idempotent reads: a caller that lost its session simply asks again), and its memory buffers are bounded in bytes. Measured on one server for a single 64 MiB answer:

| Mode | Caller time | Server heap retained afterwards | Server CPU |
|---|---|---|---|
| Classic answer, 2.5 | 634 ms | 65 MiB (kept for replay) | 266 ms |
| Classic answer, 3.0 | 602 ms | ~0 | 281 ms |
| Stream through the server | 243 ms | ~0 | 547 ms |
| Direct stream | 153 ms | 0 | 0 |

Rule of thumb: keep `query` for small answers, use `stream` for exports and long lists, add `direct()` when the volume is large enough to matter for the server, and `Page` when the user interface wants slices.

{% hint style="info" %}
To make sure a query sees a command just sent, see [Read Your Writes](read-your-writes.md).
{% endhint %}
