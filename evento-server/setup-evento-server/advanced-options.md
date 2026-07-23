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

* `evento.cluster.name`: This property defines the name of the Evento cluster. It's used for identification and helps differentiate between multiple clusters within a distributed system.
* `evento.server.instance.id`: This property assigns a unique identifier to this particular Evento server instance within the cluster. This helps differentiate between multiple running instances.

**Performance Monitoring:**

* `evento.performance.capture.rate`: This property determines the rate at which performance metrics are captured. A higher rate provides more granular data but can increase overhead.
* `evento.telemetry.ttl`: This property defines the Time To Live (TTL) for telemetry data. Telemetry data older than the specified TTL will be automatically purged from the system.

**Network Communication:**

* `server.port`: The HTTP port serving the REST API and the GUI (default `3000`).
* `evento.server.bus.port`: The TCP port on which the Evento server listens for incoming bundle message-bus connections (default `3030`). Ensure this port is accessible and not blocked by firewalls.

**Observability:**

* `management.endpoints.web.exposure.include`: Actuator endpoints exposed over HTTP; the server ships with `health,info,prometheus,metrics`, so Prometheus can scrape bus and JVM metrics from `/actuator/prometheus`.
* `management.endpoint.health.probes.enabled`: Enables Kubernetes-style liveness/readiness probes under `/actuator/health/{liveness,readiness}`. Health and info are the only endpoints that don't require authentication.

&#x20;**Event Store:**

* `evento.es.mode`: This property defines the operating mode of the Event Store. Options might be "APES" and "CPES".
* `evento.es.fetch.delay`: for the "APES" event store mode, indicates the "gray area" (inconsistency window, in milliseconds) for events due to cluster node synchronization: event fetches will not return events published after the current instant minus this value.
* `evento.es.aggregate.events.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores the current state of aggregates.
* `evento.es.aggregate.events.cache.size`: This property specifies the maximum size of the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.size`: This property defines the maximum size of the cache that stores the current state of aggregates.

**Remember:** These are just a selection of common Evento server configuration properties. The specific properties available and their meanings might vary depending on your Evento version and deployment configuration. Always refer to the official Evento documentation for the latest and most accurate information.
