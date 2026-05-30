# ConsumerStateStore

Consumer state — how far each projector, observer, and saga has progressed, plus saga instances, dead events, and dedupe windows — is what lets event consumers resume exactly where they left off after a restart without missing or reprocessing events.

{% hint style="warning" %}
**Rewritten in Evento v2.** The single v1 abstract `ConsumerStateStore` class (with its monolithic `consumeEventsFor*` / `enterExclusiveZone` / saga-state methods) has been **replaced by five small, focused SPIs**. Each concern is now independently implementable and testable. The v1 `MysqlConsumerStateStore` / `PostgresConsumerStateStore` classes are gone; durable persistence is provided by the single `evento-consumer-state-store-jdbc` module (Postgres **and** MySQL).
{% endhint %}

## The five SPIs (`evento-common`)

| SPI | Responsibility |
|---|---|
| `ConsumerStateStore` | Per-consumer checkpoint: read/commit the last processed sequence number with optimistic versioning, plus the `isEnabled(consumerId)` probe and error history. |
| `ConsumerLock` | Cross-JVM exclusive zone for a consumer. `lock(consumerId)` returns a `LockHandle` (`AutoCloseable`) so only one instance processes a consumer at a time. |
| `SagaStateStore` | Saga instance lookup by association, plus insert / update / delete of serialized saga state. |
| `DeadEventQueue` | Per-consumer dead-letter queue for events that failed processing, with a retry flag. |
| `DedupeStore` | Observer dedupe with sweep windows (at-least-once → effectively-once for fire-and-forget observers). |

These SPIs are composed by a `ConsumerProcessor`, and the trio of `ConsumerProcessor` + `ConsumerStateStore` + `DeadEventQueue` is wrapped in a `ConsumerEngineConfig` record that the bundle's consumer engines (`ProjectorEngine`, `SagaEngine`, `ObserverEngine`) run on.

## Wiring it on the bundle

You select the persistence backing with `setConsumerEngineConfigBuilder(...)` on the `EventoBundle.Builder`. The builder takes a `BiFunction<EventoServer, PerformanceService, ConsumerEngineConfig>`.

In-memory (the default — no setup, suitable for development and tests):

```java
EventoBundle.Builder.builder()
    .setBasePackage(MyApplication.class.getPackage())
    .setConsumerEngineConfigBuilder(ConsumerEngineConfig::inMemory)
    // ...
    .start();
```

When `setConsumerEngineConfigBuilder` is omitted, the bundle defaults to `ConsumerEngineConfig::inMemory` at startup.

## Implementations

* **In-memory** — `InMemoryConsumerStateStore`, `InMemoryConsumerLock`, `InMemorySagaStateStore`, `InMemoryDeadEventQueue`, `InMemoryDedupeStore` (in `evento-common`). State is lost on restart; ideal for development and tests.
* **JDBC (Postgres / MySQL)** — `JdbcConsumerStateStore`, `JdbcConsumerLock`, `JdbcSagaStateStore`, `JdbcDeadEventQueue`, `JdbcDedupeStore` (in the `evento-consumer-state-store-jdbc` module). Durable persistence backed by Flyway-managed schema. See [PostgresConsumerStateStore](postgresconsumerstatestore.md) and [MysqlConsumerStateStore](mysqlconsumerstatestore.md).
