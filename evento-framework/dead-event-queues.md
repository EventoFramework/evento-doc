# Dead Event Queues

Consistent consumers (Projectors, Sagas, and Observers) process events from the System State Store sequentially. A single event whose handler keeps failing would therefore block the whole stream — the classic *poison pill* problem. Dead Event Queues are Evento's answer: an event that cannot be processed is parked aside, the checkpoint advances, and the consumer keeps going.

## Permanent vs Transient Failures

Since Evento **2.1.1** the consumer engine distinguishes two kinds of handler failure:

* **Permanent failures** (a bug, invalid data, a violated invariant): the event is moved to the consumer's **dead event queue** together with the exception, and the consumer advances past it. This protects liveness — one poison event cannot stall the stream.
* **Transient failures** (a downed collaborator, a connection timeout, a refused or reset connection): dead-lettering these would silently *lose* work that would have succeeded moments later. Instead, the consumer's checkpoint is left in place and the event is **redelivered with exponential backoff** until the dependency recovers. Exactly-once processing is preserved across the retries by the dedupe store.

The engine classifies failures by walking the exception cause chain. You can also signal a transient failure explicitly from your own handler code by throwing (or wrapping your exception in) `TransientConsumerException` from `evento-common`:

```java
@EventHandler
void on(OrderPlacedEvent event) {
    try {
        externalClient.reserveStock(event.getOrderId());
    } catch (ExternalServiceUnavailableException e) {
        // don't dead-letter: leave the checkpoint and retry with backoff
        throw new TransientConsumerException(e);
    }
}
```

{% hint style="warning" %}
Redelivery means your handler can run more than once for the same event. Keep side effects that precede a potentially failing step **idempotent** — on redelivery they will execute again.
{% endhint %}

## Inspecting and Replaying Dead Events

Dead events are not lost — they wait in the queue with their payload and the exception that killed them:

* **Evento GUI:** the Cluster Status → Consumers tab shows each consumer's dead event queue and lets you re-enqueue events for reprocessing (e.g. after deploying a fix) or delete them.
* **Programmatically:** the `DeadEventQueue` SPI (in-memory or JDBC implementation from `evento-consumer-state-store-jdbc`) exposes the parked events; re-enqueued events are marked for retry and picked up on the consumer's next pass.

## Where the Queue Lives

The dead event queue is one of the five consumer-state SPIs composed into the `ConsumerProcessor` (see [ConsumerStateStore](eventobundle/consumerstatestore/README.md)). With the default in-memory configuration, dead events survive only as long as the process; with the [JDBC store](eventobundle/consumerstatestore/postgresconsumerstatestore.md) they are persisted in the `evento_v2_dead_event` table and shared across bundle instances.
