# EventoServerMessageBusConfiguration

This chapter covers the `EventoServerMessageBusConfiguration` class, the configuration object that tells a bundle which Evento Server cluster nodes to connect to.

{% hint style="warning" %}
**Changed in Evento v2.** In v1 this class also carried retry, reconnect, and disable back-off knobs. In v2 those concerns moved into the Netty transport layer, so `EventoServerMessageBusConfiguration` now carries **only the list of candidate cluster node addresses**. Reconnect and back-off are handled automatically (see below).
{% endhint %}

**Fields:**

* **addresses (`List<ClusterNodeAddress>`)**: The network addresses (host + port) of the Evento Server nodes the bundle can dial. The constructor takes a varargs of `ClusterNodeAddress`, so you can list multiple cluster nodes for redundancy. At least one address is required — an empty list throws `IllegalArgumentException`.

**Reconnect, retry, and back-off:**

These are no longer configured here. The v2 `BundleClient` / Netty transport reconnect automatically using an exponential back-off with jitter (base 500 ms, max 30 s, ±20%) and a heartbeat-driven liveness check. In-flight requests survive a disconnect and are retried transparently once the connection is re-established (exactly-once QoS via the broker- and bundle-side dedup caches).

**Failover, fail-back and cluster identity (2.5.0):**

The address list is **ordered, most preferred first**. A bundle fails over along the list when its server is unreachable and, with two or more addresses, **fails back** to the first one once it has been healthy for 30 s (plus jitter). Before 2.5.0 only the first address was used. Requests in flight on a server the bundle left fail at once with `BrokerChangedException` (indeterminate outcome: retry commands with an idempotency key).

* `withExpectedClusterName(String)`: refuse a server that announces another `evento.cluster.name`. This is the identity guard to use with a list.
* `withExpectedServerInstanceId(String)`: accept exactly one server. It refuses every failover target, so avoid it with more than one address.

See [Bundle Failover and Fail-back](../../evento-server/evento-server-cluster/bundle-failover-and-failback.md) for the details and the tuning knobs on `EventoBundle.Builder`.

**Example Usage:**

```java
EventoServerMessageBusConfiguration config = new EventoServerMessageBusConfiguration(
    new ClusterNodeAddress(eventoServerHost, eventoServerPort)
);
```

With multiple cluster nodes for fault tolerance:

```java
EventoServerMessageBusConfiguration config = new EventoServerMessageBusConfiguration(
    new ClusterNodeAddress("node-a", 3030),
    new ClusterNodeAddress("node-b", 3030)
).withExpectedClusterName("orders-prod");
```

**Additional Notes:**

* Specifying multiple cluster nodes in `addresses` enhances fault tolerance. If one node becomes unavailable, the bundle client dials the next node in the list, and comes back to the first one when it recovers.
* This object is passed to the `EventoBundle.Builder` via `setEventoServerMessageBusConfiguration(...)`.
