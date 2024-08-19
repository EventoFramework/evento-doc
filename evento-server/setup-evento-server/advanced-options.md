---
description: Fine Tune your Server Instances
---

# Advanced Options

Evento Server Configuration Properties

The Evento server relies on a variety of configuration properties to govern its behavior. These properties define how the server interacts with security, storage, communication, and various internal functionalities. This chapter explores some of the essential Evento server configuration properties.

**Security:**

* `evento.security.signing.key`: This property specifies the cryptographic key used for signing and verifying JWT tokens for authentication purposes. It's crucial to keep this key confidential and secure.

**Cluster:**

* `evento.cluster.name`: This property defines the name of the Evento cluster. It's used for identification and helps differentiate between multiple clusters within a distributed system.
* `evento.server.instance.id`: This property assigns a unique identifier to this particular Evento server instance within the cluster. This helps differentiate between multiple running instances.

**File Storage:**

* `evento.file.upload-dir`: This property specifies the directory path where uploaded files are stored by the server. Ensure this directory has appropriate permissions for the Evento process.

**Performance Monitoring:**

* `evento.performance.capture.rate`: This property determines the rate at which performance metrics are captured. A higher rate provides more granular data but can increase overhead.
* `evento.telemetry.ttl`: This property defines the Time To Live (TTL) for telemetry data. Telemetry data older than the specified TTL will be automatically purged from the system.

**Deployment:**

* `evento.deploy.spawn.script`: This property specifies the script path used for spawning new bundle instances. This script is typically responsible for downloading and starting the bundle code.

**Network Communication:**

* `socket.port`: This property defines the TCP port on which the Evento server listens for incoming socket connections. Ensure this port is accessible and not blocked by firewalls.

&#x20;**Event Store:**

* `evento.es.mode`: This property defines the operating mode of the Event Store. Options might be "APES" and "CPES".
* `evento.es.fetch.delay`: for "APES" event sotre mode indicates the "gray area" or "inconsistency area" for events due to cluster node syncronization. Is thelling you thet will not returns event that are published after the current instant minus this value.
* `evento.es.aggregate.events.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.expiry`: This property defines the expiration time (in milliseconds) for the cache that stores the current state of aggregates.
* `evento.es.aggregate.events.cache.size`: This property specifies the maximum size of the cache that stores fetched aggregate events.
* `evento.es.aggregate.state.cache.size`: This property defines the maximum size of the cache that stores the current state of aggregates.

**Remember:** These are just a selection of common Evento server configuration properties. The specific properties available and their meanings might vary depending on your Evento version and deployment configuration. Always refer to the official Evento documentation for the latest and most accurate information.
