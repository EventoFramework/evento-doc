---
description: Every server property and bundle setting that matters in a cluster, with its default
---

# Cluster Configuration

Server properties can also be set from the environment with Spring Boot's rule (`.` and `-` become `_`, upper case): `evento.lock.pool.maximum-size` → `EVENTO_LOCK_POOL_MAXIMUM_SIZE`.

## Server

### Identity and routing

| Property | Default | Meaning |
|---|---|---|
| `evento.cluster.name` (`EVENTO_CLUSTER_NAME`) | `evento-server` | announced to bundles in the handshake; **the same on every server of a cluster, different per deployment** |
| `evento.cluster.node.server.id` | `evento-server` | becomes `evento.server.bus.server-instance-id`; **unique per server** (requests in flight and presence rely on it; a WARN is logged while the shipped id is used) |
| `evento.server.instance.id` | `server-0` | id used by the consumer service; unique per server |
| `evento.server.bus.port` | `3030` | bundle message-bus port |
| `evento.server.bus.pick-strategy` (`EVENTO_SERVER_BUS_PICK_STRATEGY`) | `random` | `random`, `first`, or `locality-preferred` (same zone as the caller, then any) |
| `evento.server.bus.heartbeat-write-idle` / `heartbeat-read-idle` | 15 s / 45 s | server-side heartbeat |
| `evento.server.bus.auth-token` | empty | shared secret every bundle must present |

### Event store and schema

| Property | Default | Meaning |
|---|---|---|
| `spring.datasource.url` | `jdbc:postgresql://localhost:5432/evento` | the shared event store; with a PostgreSQL HA pair use a multi-host URL with `targetServerType=primary` |
| `evento.es.mode` | `CPES` | **must be `CPES` with more than one server**; `APES` is deprecated ([Event Store Modes](../setup-evento-server/evento-event-store-modes-apes-and-cpes.md)) |
| `evento.es.append.batch.writers` / `evento.es.append.batch.max-size` | -1 (2 under CPES) / 256 | group commit: appends that arrive together share one statement and one commit; `0` writers turns it off |
| `evento.server.commands.optimistic` | `true` | aggregate commands run without the lock, protected by the aggregate fence; a command that loses it runs again under the lock |
| `evento.es.fetch.concurrency` | 4 | concurrent event fetches per server |
| `evento.es.fetch.max.age.ms` | 30000 | staleness gate on fetches; ≤ 0 disables it |
| `evento.es.aggregate.{state,events}.cache.size` / `.expiry` | 1024 / 150000 ms | per-server caches, not invalidated across servers |
| `evento.es.schema.enforce-primary-key` | `true` | add the `es__events` primary key on boot; `false` is the escape hatch when duplicates exist |
| `spring.sql.init.mode` | `always` | migrate the schema with Flyway at boot (history table `evento_es_schema_history`), serialized across servers by an advisory lock; with `never`, the server changes no schema: apply the scripts in `db/upgrade/` yourself |

### Connections and locks

| Property | Default | Meaning |
|---|---|---|
| `spring.datasource.hikari.maximum-pool-size` / `minimum-idle` | 20 / 5 | application pool |
| `evento.lock.pool.maximum-size` | 10 | dedicated pool for distributed locks: the locks a server holds at once, plus up to half of it waiting in line in PostgreSQL for a lock another server holds |
| `evento.lock.pool.connection-timeout-ms` | 1000 | wait for a lock-pool connection |
| `evento.lock.acquire.timeout.ms` | 60000 | bound on every lock wait (or the command's deadline, if earlier); throws `LockAcquisitionTimeoutException` |
| `spring.task.scheduling.pool.size` | 2 | presence heartbeat and telemetry sweep do not queue behind each other |

Peak per server: 20 + 10 = **30 connections**. Three servers fit PostgreSQL's default `max_connections=100`.

### Presence

| Property | Default | Meaning |
|---|---|---|
| `evento.server.presence.heartbeat-interval-ms` | 30000 | refresh of the server's rows in `core__bundle_instance` |
| `evento.server.presence.stale-after-ms` | 180000 | after this, a presence row no longer counts as live; must be larger than the heartbeat (boot fails otherwise, warns below 3×) |

### Metrics and endpoints

* `evento.server.requests.expired{stage=queued|lock_wait|before_forward|before_append}` — commands dropped past their caller's deadline.
* `evento.server.commands.idempotent.replayed` / `.mismatched` — idempotency keys.
* `evento.server.command.phase{phase,keyed}` — per-phase latency of aggregate commands (queue, lock, story, forward, append, …); DEBUG logger `com.evento.server.es.phases` prints one line per command.
* `/actuator/health/readiness` — also gates the fail-back probes of bundles.
* `GET /api/cluster-status/zones` — zones known to this server.

## Bundle

| Setting | Default | Meaning |
|---|---|---|
| `new EventoServerMessageBusConfiguration(ClusterNodeAddress...)` | – | ordered endpoint list, most preferred first |
| `.withExpectedClusterName(String)` | none | refuse servers of another cluster |
| `.withExpectedServerInstanceId(String)` | none | accept a single server: **blocks failover**, avoid with a list |
| `EventoBundle.Builder.setZone(String)` | none | zone for `locality-preferred` routing |
| `setFailbackEnabled(Boolean)` | `null` = on with 2+ addresses | automatic return to endpoint 0 |
| `setFailbackProbeInterval(Duration)` | 5 s | probe cadence toward endpoint 0 |
| `setFailbackStabilityWindow(Duration)` | 30 s | how long endpoint 0 must stay healthy before the switch |
| `setFailbackJitter(Duration)` | 10 s | random per-instance delay added to the window |
| `setFailbackDrainTimeout(Duration)` | 10 s | wait for requests in flight before switching |
| `setHeartbeatReadIdle(Duration)` | 45 s | how long a silent server goes unnoticed |
| `setDefaultRequestTimeout(Duration)` | 30 s | request timeout, which is also the deadline the server enforces |
| `setMaxInFlightRequests(int)` | 2048 | outstanding requests per bundle |
| `setMaxInboundRequests(int)` | 0 (no bound) | requests the bundle handles at once; one more is refused at once with `TooManyPendingRequestsException`, not executed |
| `setServiceCommandOutcomeStore(ServiceCommandOutcomeStore)` | none | exactly-once for keyed service commands (shared by all instances) |
| `setComponentContexts(Class, String...)` | every context | one consumer engine per context |

See [Bundle Failover and Fail-back](bundle-failover-and-failback.md) and [Exactly-once Commands](exactly-once-commands.md) for what each setting does.

## PostgreSQL

* Version **12 or later** (the server checks at boot).
* `max_connections` ≥ servers × 30 + the sum of the bundles' pools.
* TCP keepalives (`tcp_keepalives_idle=10`, `_interval=5`, `_count=3`) and `client_connection_check_interval=5s` close orphaned backends — and the advisory locks they hold — in about 25 s after a network failure.
* For high availability of the event store, a synchronous standby (`synchronous_standby_names`) avoids losing acknowledged events on failover.
