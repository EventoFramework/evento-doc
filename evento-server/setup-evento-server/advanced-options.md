---
description: Fine Tune your Server Instances
---

# Advanced Options

Evento Server Configuration Properties

The Evento server relies on a variety of configuration properties to govern its behavior. These properties define how the server interacts with security, storage, communication, and various internal functionalities. This chapter explores some of the essential Evento server configuration properties.

**Security:**

* `spring.security.user.name` / `spring.security.user.password`: The username and password protecting the GUI and the REST API (HTTP Basic auth). Defaults are `evento` / `secret` — always override them in a real deployment.
* `spring.security.user.roles`: The roles granted to that user; the server expects `WEB,ADMIN` (the default).
* `evento.server.bus.auth-token`: Optional shared secret for the **bundle message bus**. When set, every connecting bundle must present the same token during the handshake; when blank (default), any bundle may connect.
* `evento.server.web.cors.allowed-origins`: Comma-separated list of origins allowed to call the REST API from a browser (default `*`).

**Cluster:**

* `evento.cluster.name` (env `EVENTO_CLUSTER_NAME`): The name of the Evento cluster, announced to bundles in the handshake; a bundle using `withExpectedClusterName` refuses servers of another cluster. Use the same value on every server of a cluster and a different one per deployment (the shipped `evento-server` is the same everywhere).
* `evento.cluster.node.server.id`: The unique id of this server on the bus (it becomes `evento.server.bus.server-instance-id`). **Must be unique per server** in a cluster.
* `evento.server.instance.id`: The id used by the consumer service; unique per server as well.
* `evento.server.bus.pick-strategy`: How a handler is chosen among live instances: `random` (default), `first`, or `locality-preferred` (same zone as the caller, then any).
* Distributed locks, presence and the other cluster settings are listed in [Cluster Configuration](../evento-server-cluster/cluster-configuration.md).

**Performance Monitoring:**

* `evento.performance.capture.rate`: This property determines the rate at which performance metrics are captured. A higher rate provides more granular data but can increase overhead.
* `evento.telemetry.ttl`: This property defines the Time To Live (TTL) for telemetry data. Telemetry data older than the specified TTL will be automatically purged from the system.

**Network Communication:**

* `server.port`: The HTTP port serving the REST API and the GUI (default `3000`).
* `evento.server.bus.port`: The TCP port on which the Evento server listens for incoming bundle message-bus connections (default `3030`). Ensure this port is accessible and not blocked by firewalls.

**Request Capacity:**

* `evento.server.bus.business-executor-core-size`: Threads kept alive to handle bundle requests (default `max(8, cores × 2)`).
* `evento.server.bus.business-executor-max-size`: Ceiling on those threads (default `cores × 32` since 3.0; it was `cores × 8`, which capped a 4-core server near 2,500 commands a second). The pool grows to this size *before* it queues, so this is the property that sets sustainable throughput.
* `evento.server.bus.business-executor-queue-capacity`: Requests allowed to wait for a thread (default `256`). Keep it small — a request that waits longer than its client's timeout is served for nobody. See [Throughput and Capacity](throughput-and-capacity.md).
* `evento.server.bus.business-executor-saturation-warn-interval`: Throttle for the `event=bus_business_executor_saturated` warning (default `10s`).
* `evento.es.fetch.concurrency`: Concurrent `EventFetchRequest` handlers (default `4`). Often the real ceiling on a consumer-heavy cluster; each fetch holds a full result set on heap, so raise it against measured headroom.
* `evento.es.head.poll.ms`: How often the server reads its event store's head to tell its 3.0 bundles which events were appended (default `50`). Their consumers at the head wait for that notice instead of polling, which removes the empty fetches that this concurrency limit would otherwise queue the useful ones behind. One indexed query a tick, whatever the number of consumers; reading the database keeps it right in a cluster. `0` turns it off: the server then does not offer the `head:1` capability and the consumers poll.

**Memory Bounds (3.0):**

The server keeps no query answers (queries are routed "straight": not cached, not buffered across a reconnect) and bounds what it keeps for commands in bytes:

* `evento.server.bus.dedup.max-retained-bytes`: Total bytes of command replies kept for exactly-once replays (in bytes, default `134217728` = 128 MiB); the least recently used are dropped first.
* `evento.server.bus.dedup.max-response-bytes`: A command reply larger than this (in bytes, default `1048576` = 1 MiB) is remembered as answered without its bytes; a duplicate then fails instead of executing twice.
* `evento.server.bus.reconnect-buffer.max-bytes`: Bytes of replies held for bundles that are reconnecting (in bytes, default `268435456` = 256 MiB); a reply over budget is not buffered (`event=reconnect_buffer_full`).
* `evento.server.bus.compression.threshold-bytes`: The server compresses its own replies (event fetches included) from this size, when the requester accepts it (in bytes, default `32768` = 32 KiB).

**Observability:**

* `management.endpoints.web.exposure.include`: Actuator endpoints exposed over HTTP; the server ships with `health,info,prometheus,metrics`, so Prometheus can scrape bus and JVM metrics from `/actuator/prometheus`.
* Bus capacity meters: `evento.server.bus.executor.{pool.size,max,active,queue.depth}` and the counter `evento.server.bus.executor.saturated` — the one to alert on. See [Throughput and Capacity](throughput-and-capacity.md).
* Request timers (3.0): `evento.server.request`, tagged `kind` (`query`, `service_command`, `aggregate_command`, `invocation`, `other`), `payload` and `outcome`: the time from a request reaching the server to its answer leaving it. Queries a bundle answers itself are timed by the bundle (`evento.bundle.request`).
* Consumer lag (3.0), from the server's answer to every consumer fetch, tagged `bundle`, `component`, `context`: `evento.consumer.lag.seconds` (age of the oldest event the consumer has not processed yet, growing while it is stuck: the one to alert on), `evento.consumer.lag.events` (CPES: newest sequence number minus the consumer's position, counting every context), `evento.consumer.position`, `evento.consumer.fetch.age.seconds` (time since its last fetch: a consumer that stopped). With several servers use `min by (bundle, component, context)`. `evento.consumer.lag.expiry` (default `PT15M`): series of consumers that no longer fetch through this server go away.
* `management.endpoint.health.probes.enabled`: Enables Kubernetes-style liveness/readiness probes under `/actuator/health/{liveness,readiness}`. Health and info are the only endpoints that don't require authentication.

&#x20;**Event Store:**

* `evento.es.mode`: How events are numbered: `CPES` (default) or `APES` (deprecated since 3.0). See [Event Store Modes](evento-event-store-modes-apes-and-cpes.md).
* `evento.es.fetch.delay`: APES only (deprecated): event fetches do not return events whose id is newer than the current instant minus this value (in milliseconds, default `69`).
* `evento.es.append.batch.writers`: Group commit (3.0): threads writing batches of appends, each batch in one statement and one transaction (default `-1` = automatic: 2 under CPES, 4 under APES; `0` turns group commit off).
* `evento.es.append.batch.max-size`: Most appends in one batch (default `256`).
* `evento.es.idempotency.retention`: How long idempotency keys are kept (an ISO-8601 duration such as `P30D`; unset, the default, keeps them for ever). Hourly, one server clears the keys of older events (the events stay) and deletes finished or abandoned claims. After it, a command sent again with an old key runs again: choose it longer than any retry, consumer replays included. `evento.es.idempotency.retention-interval` (default `PT1H`).
* `evento.server.commands.optimistic`: Aggregate commands run without the aggregate lock, protected by the aggregate fence, and run again under the lock when they lose it (default `true`, since 3.0; `false` takes the lock for every command, as in 2.5).
* `evento.es.aggregate.events.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores the current state of aggregates.
* `evento.es.aggregate.events.cache.size`: This property specifies the maximum size of the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.size`: This property defines the maximum size of the cache that stores the current state of aggregates.

**Remember:** These are just a selection of common Evento server configuration properties. The specific properties available and their meanings might vary depending on your Evento version and deployment configuration. Always refer to the official Evento documentation for the latest and most accurate information.
