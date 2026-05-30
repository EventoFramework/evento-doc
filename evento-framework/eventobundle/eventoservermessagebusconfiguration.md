# EventoServerMessageBusConfiguration

This chapter covers the `EventoServerMessageBusConfiguration` class, the configuration object that tells a bundle which Evento Server cluster nodes to connect to.

{% hint style="warning" %}
**Changed in Evento v2.** In v1 this class also carried retry, reconnect, and disable back-off knobs. In v2 those concerns moved into the Netty transport layer, so `EventoServerMessageBusConfiguration` now carries **only the list of candidate cluster node addresses**. Reconnect and back-off are handled automatically (see below).
{% endhint %}

**Fields:**

* **addresses (`List<ClusterNodeAddress>`)**: The network addresses (host + port) of the Evento Server nodes the bundle can dial. The constructor takes a varargs of `ClusterNodeAddress`, so you can list multiple cluster nodes for redundancy. At least one address is required — an empty list throws `IllegalArgumentException`.

**Reconnect, retry, and back-off:**

These are no longer configured here. The v2 `BundleClient` / Netty transport reconnect automatically using an exponential back-off with jitter (base 500 ms, max 30 s, ±20%) and a heartbeat-driven liveness check. In-flight requests survive a disconnect and are retried transparently once the connection is re-established (exactly-once QoS via the broker- and bundle-side dedup caches).

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
);
```

**Additional Notes:**

* Specifying multiple cluster nodes in `addresses` enhances fault tolerance. If one node becomes unavailable, the bundle client can dial another node in the list.
* This object is passed to the `EventoBundle.Builder` via `setEventoServerMessageBusConfiguration(...)`.
