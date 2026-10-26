---
description: How a bundle moves to another server, and back, without losing track of its requests
---

# Bundle Failover and Fail-back

A bundle connects to one server at a time. It uses **every** address it is given: it fails over along the list when its server dies, and fails back to the first address once that server is healthy again.

## Endpoint list

List all servers in `EventoServerMessageBusConfiguration`, **most preferred first**:

```java
var bus = new EventoServerMessageBusConfiguration(
        new ClusterNodeAddress("evento-a", 3030),   // preferred: this site's / cell's server
        new ClusterNodeAddress("evento-b", 3030),
        new ClusterNodeAddress("evento-c", 3030))
    .withExpectedClusterName("orders-prod");

EventoBundle.Builder.builder()
    .setEventoServerMessageBusConfiguration(bus)
    // ...
    .start();
```

{% hint style="info" %}
A bundle fails back to the first entry by default: put the bundle's local server first.
{% endhint %}

* A session that fails **before** it is ready moves to the next endpoint (round robin, backoff counted per pass over the list). `start()` fails only once every endpoint was tried.
* A session that was ready and drops restarts from endpoint 0.
* In a single-site HA deployment give **every** bundle the same list in the same order, so they all prefer the same server (a request needs caller and handler on the same server). In a cell deployment each bundle lists its own cell's server first.

## Cluster identity

Every server announces `evento.cluster.name` in its handshake. A bundle that sets `withExpectedClusterName(...)` refuses any server announcing another name (or none) and keeps dialing the next endpoint (`event=cluster_name_mismatch`). This protects against a bundle joining the wrong environment.

* Set `evento.cluster.name` (env `EVENTO_CLUSTER_NAME`) per deployment: the shipped default `evento-server` is the same on every stock server, so requiring it protects nothing (the server logs `event=cluster_name_shipped_default` while it keeps it).
* Do **not** use `withExpectedServerInstanceId(...)` with an endpoint list: it accepts exactly one server and therefore refuses every failover target.
* Give each server a unique `evento.cluster.node.server.id`: requests in flight and presence tracking rely on it.

## Requests in flight

When the bundle reconnects to a **different** server, the requests it had sent through the old one can no longer be answered (the old server would replay their replies only to a bundle that comes back to *it*). They fail at once with **`BrokerChangedException`** instead of waiting for the full request timeout.

`BrokerChangedException` extends `RequestTimeoutException`: the outcome is **indeterminate**, the command may or may not have been applied. Retry commands only with an [idempotency key](exactly-once-commands.md); queries can be retried freely.

A request the bundle refused **before writing anything** (between two sessions, or while draining for a fail-back) fails with **`RequestNotSentException`** (`SendFailedException` on the low-level client): nothing was executed, so it is always safe to retry.

Reconnecting to the **same** server keeps the 2.x behaviour: pending requests survive the reconnect.

## Fail-back

After a failover a bundle does not stay on the fallback server: left there, a whole cell would keep crossing the WAN after a server restart, and callers and handlers of one cell could end up on different servers. With two or more endpoints a bundle comes back on its own:

1. While connected to any endpoint but 0, it **probes** endpoint 0 every 5 s with a TCP connect and a transport `Ping`. A probe sends no `Hello`: it never registers the bundle or steals a session. The server answers probes only once it is **ready** (Spring `ACCEPTING_TRAFFIC`: JPA and the event store up), not as soon as its port is open.
2. When endpoint 0 has answered every probe for the **stability window** (30 s) plus a random per-instance **jitter** (0–10 s), the bundle switches: new outbound requests are refused (`RequestNotSentException`, safe to retry), the bundle disables itself on the current server, waits up to the **drain timeout** (10 s) for requests in flight in both directions, then closes the session and dials endpoint 0 without backoff. Requests still pending after the drain fail with `BrokerChangedException`.
3. Bundles that handle no requests (gateways, pure callers) wait the whole jitter range on top, so that a cell's handlers are back before its callers.
4. **Reactive fail-back:** if the current server answers `no handler for` while endpoint 0 answers probes, the bundle switches at once (`event=failback_reactive`): in an HA pair the fallback has no handler left once the cell's handlers are home. The cost is one failed request per caller, not a whole window.

A failed probe restarts the window, so a flapping server never gets the bundles back. If the handshake on endpoint 0 fails (e.g. a cluster-name mismatch) the bundle lands on the next endpoint and the next window doubles (up to 16×); after three refusals in a row fail-back is suspended (`event=failback_suspended`, ERROR) until a session on endpoint 0 succeeds by other means or the process restarts — fix the configuration it names.

Log events: `failback_started`, `failback_drained`, `failback_reactive`, `failback_completed`, `failback_failed`, `failback_suspended`. Counters: `BundleClient.failbacksCompleted()`, `failbacksFailed()`, `reactiveFailbacks()`.

### Configuration

```java
EventoBundle.Builder.builder()
    .setFailbackEnabled(true)                          // null (default) = on with 2+ addresses
    .setFailbackProbeInterval(Duration.ofSeconds(5))
    .setFailbackStabilityWindow(Duration.ofSeconds(30))
    .setFailbackJitter(Duration.ofSeconds(10))
    .setFailbackDrainTimeout(Duration.ofSeconds(10))
```

`setFailbackEnabled(false)` restores the 2.4 behaviour (stay on the fallback until the session drops).

{% hint style="info" %}
**Fail-back needs the address list.** With a single address behind a load balancer (a VIP with the active server as primary and the others as backup), new connections go back to the primary, but sessions already open on a backup stay there: the bundle has no "endpoint 0" to probe. Restart the bundles left on the backup, or prefer the list.
{% endhint %}

## Detecting a dead server

A server that dies cleanly closes its sockets and the bundle notices at once. A silent partition (no RST) is noticed only after the heartbeat **read-idle** time, 45 s by default. Lower it on the bundle if you need faster detection:

```java
.setHeartbeatReadIdle(Duration.ofSeconds(15))   // also lowers the ping cadence to a third
```

Other link settings on `EventoBundle.Builder`: `setTransportConfig`, `setReconnectStrategy`, `setDefaultRequestTimeout` (30 s), `setMaxInFlightRequests` (2048).

## Timings

| Phase | Typical duration |
|---|---|
| Failover | detection (immediate with RST, up to read-idle without) + reconnect backoff + handshake + registration: **10.3 s** measured for a cell whose server was killed |
| Fail-back | server ready + first probe (≤ 5 s) + window (30 s) + jitter (0–10 s) [+ 10 s for bundles without handlers, or immediately on the first `no handler for`] + drain (≤ 10 s); the interruption seen by one bundle is about drain + handshake |
