# InMemoryConsumerStateStore

The in-memory consumer state implementation keeps all consumer state — checkpoints, locks, saga instances, dead events, and dedupe windows — in concurrent in-process collections. Because nothing is persisted, state is lost on application restart, which makes it ideal for development, tests, and demos where durability is not a concern.

{% hint style="warning" %}
**Changed in Evento v2.** There is no longer a single `InMemoryConsumerStateStore` class wired via `setConsumerStateStoreBuilder`. The in-memory backing is now the set of in-memory implementations of the five consumer SPIs, composed for you by `ConsumerEngineConfig.inMemory(...)`. See [ConsumerStateStore](README.md) for the SPI overview.
{% endhint %}

## In-memory implementations (`evento-common`)

| SPI | In-memory implementation |
|---|---|
| `ConsumerStateStore` | `InMemoryConsumerStateStore` |
| `ConsumerLock` | `InMemoryConsumerLock` |
| `SagaStateStore` | `InMemorySagaStateStore` |
| `DeadEventQueue` | `InMemoryDeadEventQueue` |
| `DedupeStore` | `InMemoryDedupeStore` |

## Usage

In-memory is the default backing. You can set it explicitly with the `ConsumerEngineConfig::inMemory` factory:

```java
EventoBundle.Builder.builder()
    .setBasePackage(MyApplication.class.getPackage())
    .setConsumerEngineConfigBuilder(ConsumerEngineConfig::inMemory)
    // ...
    .start();
```

If you omit `setConsumerEngineConfigBuilder` entirely, the bundle falls back to `ConsumerEngineConfig::inMemory` at startup, so the call above is equivalent to leaving it unset.

{% hint style="warning" %}
**Important.** All checkpoints, saga state, dead events, and dedupe windows live only in memory and are lost when the JVM restarts. For production, use the durable JDBC backing — see [PostgresConsumerStateStore](postgresconsumerstatestore.md) or [MysqlConsumerStateStore](mysqlconsumerstatestore.md).
{% endhint %}
