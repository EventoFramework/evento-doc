# MySQL Consumer State Store (JDBC)

For durable consumer state on MySQL, use the JDBC implementations of the five consumer SPIs from the `evento-consumer-state-store-jdbc` module, selecting the `MYSQL` SQL dialect. It is the same module used for PostgreSQL — only the `SqlDialect` differs.

{% hint style="warning" %}
**Rewritten in Evento v2.** The v1 single-class `MysqlConsumerStateStore` (with its `init()` DDL and `evento__consumer_state` tables) no longer exists. MySQL support now lives in the `evento-consumer-state-store-jdbc` module, shared with Postgres via a `SqlDialect`. Schema is created by Flyway migrations (tables `evento_v2_consumer_state`, `evento_v2_saga_state`, `evento_v2_dead_event`, `evento_v2_dedupe`) — there is no manual `init()` call.
{% endhint %}

## Dependency

```gradle
implementation group: 'com.eventoframework', name: 'evento-consumer-state-store-jdbc', version: '2.3.0'
```

## Schema migration

Run the bundled Flyway migrations against your `DataSource` once at startup:

```java
FlywayMigrator.migrate(dataSource, SqlDialect.MYSQL);
```

`JdbcConsumerLock` uses MySQL's `GET_LOCK(id, 0)` for the cross-JVM exclusive zone, and `JdbcSagaStateStore` stores saga state as JSON with a flat `associations` column for fast `JSON_EXTRACT` lookups.

## Wiring the bundle

Compose the five JDBC stores into a `ConsumerProcessor`, wrap it in a `ConsumerEngineConfig`, and pass the builder to `setConsumerEngineConfigBuilder`:

```java
BiFunction<EventoServer, PerformanceService, ConsumerEngineConfig> jdbcConfig =
    (eventoServer, performanceService) -> {
        var dialect       = SqlDialect.MYSQL;
        var lock          = new JdbcConsumerLock(dataSource, dialect);
        var stateStore    = new JdbcConsumerStateStore(dataSource, dialect);
        var sagaStore     = new JdbcSagaStateStore(dataSource, dialect, objectMapper);
        var deadEventQueue = new JdbcDeadEventQueue(dataSource, dialect, objectMapper);
        var dedupeStore   = new JdbcDedupeStore(dataSource, dialect);
        var processor = ConsumerProcessor.builder()
                .eventoServer(eventoServer)
                .lock(lock)
                .stateStore(stateStore)
                .sagaStateStore(sagaStore)
                .deadEventQueue(deadEventQueue)
                .dedupeStore(dedupeStore)
                .performanceService(performanceService)
                .observerExecutor(Executors.newVirtualThreadPerTaskExecutor())
                .build();
        return new ConsumerEngineConfig(processor, stateStore, deadEventQueue);
    };

EventoBundle.Builder.builder()
    .setBasePackage(MyApplication.class.getPackage())
    .setConsumerEngineConfigBuilder(jdbcConfig)
    // ...
    .start();
```

{% hint style="info" %}
Provide a pooled `DataSource` (e.g. HikariCP). The optimistic-versioning checkpoint commit and the `GET_LOCK`-based exclusive zone give safe behaviour when multiple instances of the same bundle run concurrently — only one instance processes a given consumer at a time.
{% endhint %}
