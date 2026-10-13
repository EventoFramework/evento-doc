---
description: Several Evento Servers on one PostgreSQL event store, from one site to three continents
---

# Evento Server Cluster

Evento Server can run as a **cluster**: several server instances share one PostgreSQL event store and one component catalog, and bundles move between them when a server dies or comes back. Since **2.5.0** the cluster mode is production-ready: bundles fail over *and* fail back on their own, commands can be made exactly-once across retries and servers, distributed locks are bounded, and requests are routed to the closest handler.

This section explains how the cluster works and how to deploy it:

| Page | What it covers |
|---|---|
| [Bundle Failover and Fail-back](bundle-failover-and-failback.md) | endpoint lists, cluster identity, what happens to requests in flight, the automatic return to the preferred server |
| [Exactly-once Commands](exactly-once-commands.md) | idempotency keys, keys derived for sagas/projectors/observers, the service outcome store, caller deadlines |
| [Cells and Locality](cells-and-locality.md) | one server per site, zones and `locality-preferred` routing, presence and the shared catalog |
| [Cluster Configuration](cluster-configuration.md) | every server property and bundle setting that matters in a cluster, with defaults |
| [Upgrading to 2.5](upgrading-to-2-5.md) | rollout order, first-boot schema migrations, connection sizing |

## How a cluster works

<figure><img src="../../.gitbook/assets/image (50).png" alt=""><figcaption><p>Several servers, one shared PostgreSQL</p></figcaption></figure>

* **One shared state.** Every server reads and writes the same `es__events` table and the same catalog (`core__bundle`, `core__component`, `core__handler`, `core__consumer`, `core__bundle_instance`). A consumer can fetch from any server, and its checkpoint and lane lock live in the consumer state store, so a lane survives a change of server.
* **Each server routes to its own bundles.** Handler registry, forwarding table and correlations live in the server's memory, and servers do not forward requests to each other. A request reaches a handler only when caller and handler are connected to the **same** server; otherwise it fails at once with `no handler for <PayloadType>`. This is a design choice: connectivity is regional, a client may reach only some servers, and the intended topology is a **cell** — a server with a complete set of handlers next to it. Requests stay in the cell, a failure stays in the cell, and consistency between cells comes from the shared event store.
* **Global ordering is preserved.** Appends run in one statement under a PostgreSQL advisory lock (`CPES` mode), so the sequence order equals the commit order on every server, and aggregate commands are mutually excluded cluster-wide by distributed locks.

{% hint style="warning" %}
**Use `evento.es.mode=CPES` with more than one server** (it is the value the server ships with). `APES` relies on a time window that does not hold across servers.
{% endhint %}

## Topologies

The cluster grows one level at a time; each level keeps the rules of the previous one.

| Level | Shape | Use it when |
|---|---|---|
| **Single server** | one server, one PostgreSQL, all bundles | development, small deployments |
| **Server HA** | 2–3 servers on one site and one database; every bundle lists the servers **in the same order**, so all of them prefer the same server and the others are hot standbys | a server crash or restart must not stop the application |
| **Cells** | one server per site (EU, AM, APAC…), each with a complete set of command and query handlers; bundles list their own cell's server first; `locality-preferred` routing | users on several sites should get answers from a nearby broker |
| **Regions as contexts** | cells plus regional application databases; events carry the region as their [context](../../evento-framework/eventobundle/context.md) and each cell consumes its own regions | data must stay in its region, with a few global events |

PostgreSQL high availability (multi-host JDBC URLs with `targetServerType=primary`, a synchronous standby for the event store) applies to every level from Server HA up.

{% hint style="info" %}
Server HA is **active/passive for the bus**, not load balancing between servers: a request needs caller and handler on the same server, so all bundles of a site prefer the same one. Scale handlers out by running more instances of a bundle; the server picks among the live ones.
{% endhint %}

## Measured behaviour

The cluster mode was validated on a three-continent lab (7 regions, simulated WAN at 80–150 ms RTT to the event-store primary, chaos scenarios against 2.4.6 and 2.5.0):

| Measure | 2.4.6 | 2.5.0 |
|---|---|---|
| Commands confirmed, 7 regions × 20 orders/min | 227/319 | **492/492** |
| Cell left without its server: first acknowledged command | never (0/18) | **10.3 s** |
| Requests in flight on a dead server, failed only after ≥ 25 s | 24/24 | **0** (`BrokerChangedException` at once) |
| Payments executed twice across server failures | yes | **0** (idempotency keys + outcome store) |
| Cold starts needing a catalog repair | 7/7 | **0/7** |
| Consumers wiped by a stale server after a pause | 10 | **0** |

The latency of a command is dominated by round trips to the event-store primary: p50 ≈ 7 ms locally, ≈ 0.1–0.3 s in the primary's cell, ≈ 0.7 s at 80 ms RTT and ≈ 1.2 s at 150 ms RTT. Put the primary in the cell with the most writes.

## Checklist

* [ ] Every server: the same database, `evento.es.mode=CPES`, the same `evento.cluster.name`, a **unique** `evento.cluster.node.server.id` and `evento.server.instance.id`.
* [ ] Every bundle: the full list of server addresses, its own (or the site's active) server first, and `withExpectedClusterName(...)`.
* [ ] Every cell hosts every handler its callers use (commands, queries, and commands sent by sagas).
* [ ] Callers treat `BrokerChangedException` / `RequestTimeoutException` as *indeterminate* and retry commands **with an idempotency key**.
* [ ] PostgreSQL `max_connections` ≥ servers × 30 + the bundles' pools (see [Upgrading to 2.5](upgrading-to-2-5.md)).
* [ ] PostgreSQL 12 or later, JDK 25.0.3 or later.

**Security:** all servers share one database, so protect it like the event store it is, and set `evento.server.bus.auth-token` so that only your bundles can join the bus.
