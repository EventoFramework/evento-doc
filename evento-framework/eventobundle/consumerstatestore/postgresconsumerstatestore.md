# Postgres Consumer State Store (JDBC)

For durable consumer state on PostgreSQL, use the JDBC implementations of the five consumer SPIs from the `evento-consumer-state-store-jdbc` module, selecting the `POSTGRES` SQL dialect.

{% hint style="warning" %}
**Rewritten in Evento v2.** The v1 single-class `PostgresConsumerStateStore` (with its `init()` DDL and `evento__consumer_state` tables) no longer exists. Postgres support now lives in the `evento-consumer-state-store-jdbc` module, shared with MySQL via a `SqlDialect`. Schema is created by Flyway migrations (tables `evento_v2_consumer_state`, `evento_v2_saga_state`, `evento_v2_dead_event`, `evento_v2_dedupe`) — there is no manual `init()` call.
{% endhint %}

## Dependency

```gradle
implementation group: 'com.eventoframework', name: 'evento-consumer-state-store-jdbc', version: '2.0.0'
```

## Schema migration

{% hint style="info" %}
**Changed in Evento v2.1.1.** The JDBC store now **auto-creates its schema on first connection** — no manual migration step is needed. `JdbcConsumerStateStore` runs `FlywayMigrator.migrate(dataSource, dialect)` once on first connect (idempotent, tracked in a dedicated `evento_v2_schema_history` table) via the default `autoMigrate=true`. To opt out — e.g. when you apply the schema out-of-band with your own Flyway run that includes `SqlDialect.migrationLocation()` — use the 3-arg constructor `new JdbcConsumerStateStore(dataSource, dialect, false)`. On versions **before 2.1.1** you must still run the migration yourself before constructing the store.
{% endhint %}

On Evento **before v2.1.1**, run the bundled Flyway migrations against your `DataSource` once at startup, before constructing the store:

```java
FlywayMigrator.migrate(dataSource, SqlDialect.POSTGRES);
```

`JdbcConsumerLock` uses Postgres advisory locks (`pg_try_advisory_lock(hashtext(id))`) for the cross-JVM exclusive zone, and `JdbcSagaStateStore` stores saga state as JSONB with a flat `associations` column for fast `->> ?` lookups.

## Wiring the bundle

Compose the five JDBC stores into a `ConsumerProcessor`, wrap it in a `ConsumerEngineConfig`, and pass the builder to `setConsumerEngineConfigBuilder`:

```java
BiFunction<EventoServer, PerformanceService, ConsumerEngineConfig> jdbcConfig =
    (eventoServer, performanceService) -> {
        var dialect       = SqlDialect.POSTGRES;
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
Provide a pooled `DataSource` (e.g. HikariCP). The optimistic-versioning checkpoint commit and the advisory-lock exclusive zone give safe behaviour when multiple instances of the same bundle run concurrently — only one instance processes a given consumer at a time.
{% endhint %}
