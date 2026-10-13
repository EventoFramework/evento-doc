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
* `evento.server.bus.business-executor-max-size`: Ceiling on those threads (default `cores × 8`). The pool grows to this size *before* it queues, so this is the property that sets sustainable throughput.
* `evento.server.bus.business-executor-queue-capacity`: Requests allowed to wait for a thread (default `256`). Keep it small — a request that waits longer than its client's timeout is served for nobody. See [Throughput and Capacity](throughput-and-capacity.md).
* `evento.server.bus.business-executor-saturation-warn-interval`: Throttle for the `event=bus_business_executor_saturated` warning (default `10s`).
* `evento.es.fetch.concurrency`: Concurrent `EventFetchRequest` handlers (default `4`). Often the real ceiling on a consumer-heavy cluster; each fetch holds a full result set on heap, so raise it against measured headroom.

**Observability:**

* `management.endpoints.web.exposure.include`: Actuator endpoints exposed over HTTP; the server ships with `health,info,prometheus,metrics`, so Prometheus can scrape bus and JVM metrics from `/actuator/prometheus`.
* Bus capacity meters: `evento.server.bus.executor.{pool.size,max,active,queue.depth}` and the counter `evento.server.bus.executor.saturated` — the one to alert on. See [Throughput and Capacity](throughput-and-capacity.md).
* `management.endpoint.health.probes.enabled`: Enables Kubernetes-style liveness/readiness probes under `/actuator/health/{liveness,readiness}`. Health and info are the only endpoints that don't require authentication.

&#x20;**Event Store:**

* `evento.es.mode`: This property defines the operating mode of the Event Store. Options might be "APES" and "CPES".
* `evento.es.fetch.delay`: for the "APES" event store mode, indicates the "gray area" (inconsistency window, in milliseconds) for events due to cluster node synchronization: event fetches will not return events published after the current instant minus this value.
* `evento.es.aggregate.events.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores the current state of aggregates.
* `evento.es.aggregate.events.cache.size`: This property specifies the maximum size of the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.size`: This property defines the maximum size of the cache that stores the current state of aggregates.

**Remember:** These are just a selection of common Evento server configuration properties. The specific properties available and their meanings might vary depending on your Evento version and deployment configuration. Always refer to the official Evento documentation for the latest and most accurate information.
