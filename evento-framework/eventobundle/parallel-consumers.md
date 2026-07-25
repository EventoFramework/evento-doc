---
description: Consuming events in parallel with bounded executors
---

# Parallel Consumers

By default a consumer is strictly sequential: it fetches a batch of events, hands one to the handler, **waits for it to return**, records the checkpoint, and moves on. That is the right default — it makes ordering and delivery guarantees simple — but it means throughput is capped by handler latency, even for handlers whose effect does not depend on order.

Since Evento **2.4.0** an `@EventHandler` can name a *consumer executor* and be dispatched to it, so events are handled **in parallel** up to that executor's capacity.

## Declaring an executor

Executors are registered on `EventoBundle.Builder`, in the same spirit as [contexts](context.md) — deployment configuration, not something the handler's code can carry:

<pre class="language-java"><code class="lang-java">EventoBundle.Builder.builder()
...
<strong>.addConsumerExecutor(ConsumerExecutors.virtual("read-model", 64))
</strong><strong>.addConsumerExecutor(ConsumerExecutors.pooled("tx-writer", 8))
</strong>...
</code></pre>

A handler then references one by name:

```java
@Projector(version = 1)
public class OrderViewProjector {

    // unchanged: sequential, one event at a time
    @EventHandler
    void on(OrderCreated event) { … }

    // dispatched to the "read-model" executor, up to 64 at a time
    @EventHandler(executor = "read-model", retry = 3)
    void on(OrderTotalRecomputed event) { … }
}
```

A name is a **shared capacity budget for the whole bundle**: every handler naming `read-model` competes for the same 64 permits. That is deliberate — it lets you cap total concurrency against a downstream resource in one place.

Referencing an executor that was never registered **fails bundle start-up**. A typo would otherwise degrade silently to sequential execution: the handler still works, just slower, and the missing parallelism only shows up later as a throughput mystery.

| Factory | Backing | Use for |
| --- | --- | --- |
| `ConsumerExecutors.virtual(name, n)` | virtual threads, `n` permits | I/O-bound handlers — the usual choice |
| `ConsumerExecutors.pooled(name, n)` | fixed platform-thread pool | CPU-bound handlers, or a handler pinning a native resource |
| `ConsumerExecutors.partitioned(name, lanes)` | virtual threads, one task per lane | handlers that need [per-aggregate ordering](#keeping-order-per-aggregate) |

## What you give up

This is the part to read before adopting it.

{% hint style="warning" %}
Parallel dispatch relaxes two guarantees. Use it only where the handler is **idempotent** or a **blind overwrite** (upsert a row, set a cache key, fire a notification) — or use a [partitioned executor](#keeping-order-per-aggregate) to get ordering back.
{% endhint %}

* **Order.** Two events — including two events on the same aggregate — may be applied out of sequence order.
* **At-least-once delivery, for events in flight.** The consumer checkpoint advances when a task **starts**, not when it finishes. If the JVM dies abruptly, events whose handler was mid-flight are not redelivered. A graceful shutdown drains them; a `kill -9` does not.

The "checkpoint on start" rule is what makes the whole design safe in the other direction. Because the checkpoint tracks the dispatch frontier, the consumer can never run more than the executor's capacity ahead of completion — it can never enqueue an unbounded prefix of the event store, and the crash-loss window is bounded by the number of *running* tasks rather than by a queue depth. When the executor is saturated the consume cycle simply ends early and resumes next time.

### `retry = -1` means `0` under an executor

`retry` defaults to `-1`, which on the sequential path means *retry forever*. Inside a parallel task that would pin a concurrency permit indefinitely and starve every other handler sharing the executor, so under an executor it is **coerced to `0`**: one attempt, then the [dead event queue](../dead-event-queues.md).

{% hint style="info" %}
An async handler with default settings therefore dead-letters on its **first** failure, transient ones included. Set an explicit `retry` for any parallel handler that touches a remote dependency.
{% endhint %}

More broadly, transient failures behave differently here. On the sequential path a transient failure leaves the checkpoint alone and the event is redelivered; in a parallel task the checkpoint has already advanced, so redelivery is no longer available and the event dead-letters once the retry budget is exhausted. The consumer detects a run of transient failures and backs its fetch loop off exponentially, so a downed dependency does not burn the whole stream into the dead event queue at full speed.

### Not available on sagas

`@SagaEventHandler` has no `executor` attribute. A saga handler is a read-modify-write on shared saga state, which parallel dispatch would corrupt.

## Keeping order per aggregate

Most read-model projectors are not idempotent, but they *are* sequential per aggregate — read a row, modify it, write it back. A **partitioned** executor covers exactly that case: events sharing an ordering key (the event's aggregate id) are pinned to one lane and applied in sequence order, while different aggregates run in parallel.

```java
.addConsumerExecutor(ConsumerExecutors.partitioned("read-model", 32))
```

Nothing changes in the handler — the consume loop already passes the aggregate id as the ordering key, and only a partitioned executor acts on it.

A lane runs one task at a time and a submission whose lane is busy waits for it rather than queueing behind it, so a burst on one hot aggregate serialises. That is the ordering guarantee doing its job, not a defect. Concurrency is bounded by the lane count and reduced further by key skew, so choose `lanes` well above the number of aggregates you expect to be active at once.

## Getting at-least-once back

If losing in-flight events on a hard kill is unacceptable, switch the consumer's checkpoint mode:

```java
.setCheckpointMode(CheckpointMode.WATERMARK)
// or, per projector:
.setComponentCheckpointMode(OrderViewProjector.class, CheckpointMode.WATERMARK)
```

| Mode | Checkpoint records | After a crash |
| --- | --- | --- |
| `ON_START` (default) | the dispatch frontier | in-flight events are **lost** |
| `WATERMARK` | the highest **contiguous completed** sequence | in-flight events are **replayed** |

Under `WATERMARK` the persisted checkpoint deliberately lags behind running work, while the fetch cursor still follows the dispatch frontier — so nothing is processed twice *within* a run; only a crash replays, and only the window between the two. Those duplicates are precisely what idempotent handlers already tolerate.

Two consequences worth knowing:

* A handler that never returns pins the watermark, so the persisted checkpoint stops advancing while the consumer runs on. The replay cost on restart grows with that gap; the framework logs a warning when it gets large.
* The consumer's "last event" figure in the GUI trails true progress by the in-flight window, because the checkpoint now means *completed* rather than *started*.

## Sizing against a database

If your handlers open a transaction — typically through a `MessageHandlerInterceptor` — each **running** handler holds a pooled connection for its whole task, on top of the one connection every active consumer already pins for its lock. Size the pool for:

```
concurrent consumers + Σ(capacity of each executor used by transactional handlers) + headroom
```

{% hint style="danger" %}
An executor of capacity 64 against a 10-connection pool does not fail loudly. It surfaces as connection-acquisition timeouts, which the consumer classifies as transient — and with the default `retry` those dead-letter on the first hit. Cap a transactional handler's executor at its share of the pool.
{% endhint %}

Transaction management from an interceptor keeps working unchanged under parallel dispatch. For any single event, `before → handler → after/onException` always run on **one and the same thread** — the executor's task thread — so `ThreadLocal`-bound transaction managers behave exactly as they do sequentially, and each retry attempt gets its own transaction. Two obligations on the interceptor: it is now entered concurrently, so keep per-invocation state in `ThreadLocal`s rather than instance fields, and unbind in a `finally`, because a dead-event write happens on the same thread right after `onException` returns.

## Observing it

* **Evento GUI** — the Component Catalog marks each parallel handler with its executor, and Cluster Status → Consumers shows a *Parallel* row with the executor names, in-flight count, saturation count and transient-failure count.
* **Prometheus** — bundles push their counters to the server, which exposes them on `/actuator/prometheus`:
  * `evento.consumer.executor.{capacity,in.flight,admitted,rejected,completed,failed}` tagged `bundle,instance,executor`
  * `evento.consumer.async.{in.flight,submit.timeouts,transient.failures}` tagged `bundle,instance,consumer,component`

{% hint style="info" %}
`evento.consumer.executor.rejected` is the one to alert on. It counts submissions refused for lack of capacity — the executor telling you it is the bottleneck.
{% endhint %}

A bundle that registers no executor pushes nothing and behaves exactly as before, so none of this costs anything until you opt in.
