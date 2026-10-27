---
description: A query that is answered only once the projections reflect a given write
---

# Read Your Writes

Projections are eventually consistent: a command is confirmed as soon as its event is stored, while the projector that updates the read model processes it a moment later. A user who saves a form and is redirected to the list right away can therefore see the list *without* what they just saved.

Since Evento **3.0** a query can require to **see a given write**. It is answered only once the answering bundle's projectors have processed that event, or fails explicitly when they cannot catch up in time: it never answers stale.

## Tracking a command

`CommandGateway.sendTracked(...)` sends a command like `send` and also returns where its event was stored, as a `ConsistencyToken`:

```java
Tracked<OrderPlaced> tracked = commandGateway.<OrderPlaced>sendTracked(new PlaceOrderCommand(orderId, items))
        .get();

OrderPlaced event = tracked.result();
ConsistencyToken token = tracked.token();
```

A query that carries the token waits for it:

```java
Single<OrderView> order = queryGateway.queryWith(new FindOrderQuery(orderId),
        QueryOptions.defaults().after(token).timeout(Duration.ofSeconds(5)))
    .get();
```

`queryWith(query, QueryOptions)` is the query method that takes options (timeout, metadata, consistency); `stream(query, options)` accepts the same requirement.

## Every write of this process

When the code asking the query is the same process that sent the commands, there is no need to carry tokens around:

```java
queryGateway.queryWith(new ListOrdersQuery(customerId), QueryOptions.defaults().readYourWrites());
```

covers every write this bundle has made so far.

## Across processes

A token is a small value that survives a round trip as text, for example in an HTTP header sent to the browser and back with its next request:

```java
response.setHeader("X-Evento-Consistency", tracked.token().encode());

// next request, possibly on another instance
var token = ConsistencyToken.parse(request.getHeader("X-Evento-Consistency"));
queryGateway.queryWith(query, QueryOptions.defaults().after(token));
```

Tokens combine with `merge`.

## How it behaves

* Positions are kept **per context**: a token carries, for each [context](../../eventobundle/context.md), the last event written there. A projector waits only for the contexts it reads, so a projector of `eu` is never made to wait for an event of `us`; a projector reading every context waits for the highest position.
* The answering bundle **wakes its projectors** instead of letting them finish their idle pause, so the wait is about the time it takes to process the event, not the polling interval. When another instance holds the projector's lane, it reads the shared checkpoint.
* If the projectors do not catch up, the query fails with `ConsistencyTimeoutException` (naming the projector that lagged) just before the caller's deadline, rather than answer stale.
* With projectors dispatched to an [executor](../../eventobundle/parallel-consumers.md) (`@EventHandler(executor = …)`), the guarantee needs `CheckpointMode.WATERMARK`: by default the checkpoint advances when a task starts, not when it completes.
* A gateway implementation that does not support it refuses a consistency requirement (and `sendTracked`) instead of silently ignoring it.

{% hint style="info" %}
Read-your-writes waits only for **projectors**. It does not make a federated query (a query handler that asks other queries) consistent across services: see the warning in [@QueryHandler](queryhandler.md).
{% endhint %}
