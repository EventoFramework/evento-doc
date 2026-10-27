---
description: One server per site, zones and locality-aware routing, presence and the shared catalog
---

# Cells and Locality

When users are spread over several sites, give each site its own server — a **cell** — so that commands and queries enter the cluster close to the user. All cells share the same event store, so they stay consistent; the price is that an append from a remote cell pays the round trips to the event-store primary.

## A complete set of handlers per cell

Each server routes only to the bundles connected to it (see [How a cluster works](README.md#how-a-cluster-works)). Therefore:

* every cell must host **every handler its callers use**: command handlers, query handlers, and the handlers of commands that sagas send;
* pure consumers (projectors, observers) can run anywhere: event fetches are served by any server from the shared `es__events`.

A cell missing a handler answers `no handler for <PayloadType>` within milliseconds, even if the handler is alive in another cell.

```
cell EU (zone EU)              cell AM (zone AM)              cell APAC (zone APAC)
  gateways ─┐                    gateways ─┐                    gateways ─┐
  order-command ─ evento-eu      order-command ─ evento-am      order-command ─ evento-apac
  order-query  ─┘     │          order-query  ─┘     │          order-query  ─┘     │
                      └──────────── PostgreSQL primary (EU) ◄────────────────────────┘
```

Each bundle lists **its own cell's server first**, then the others as failover targets.

## Locality-aware routing

A bundle declares where it runs:

```java
EventoBundle.Builder.builder()
    .setZone("EU")
    // ...
```

The zone travels as a `zone:EU` capability in the handshake (no new wire field; older servers ignore it). A server started with

```properties
evento.server.bus.pick-strategy=locality-preferred
```

routes each request to an available handler **in the same zone as the bundle that sent it**, and falls back to any available handler when that zone has none — so a dead region costs latency, not availability. Commands brokered for a saga or a gateway are picked on behalf of the original sender. The default strategy stays `random` (`first` is also available).

This matters after a failover: when the APAC bundles land on `evento-eu`, that server sees an EU and an APAC instance of the same handler. With `locality-preferred` EU callers keep using the EU handler and APAC callers the APAC one; with `random` half the commands would cross the WAN twice.

`GET /api/cluster-status/zones` lists the instance → zone map a server knows.

## Presence and the shared catalog

Servers share one catalog but each sees only its own connections. Two mechanisms keep the catalog correct when bundles move:

* **Presence.** The table `core__bundle_instance` records which server holds each bundle instance's session. A server cleans up an instance's catalog rows only if it still owns it, so a late disconnect noticed by the old server no longer wipes a bundle that already moved to another server. Each server refreshes its rows every `evento.server.presence.heartbeat-interval-ms` (30 s); rows older than `evento.server.presence.stale-after-ms` (3 min) stop counting as live, so a server that crashes for good cannot keep its bundles in the catalog. The server refuses to boot if the stale time is not larger than the heartbeat.
* **Per-bundle components.** Components are keyed per bundle (`bundleId:componentName`), so the same projector class deployed by several bundles (one per region) keeps one row each. Concurrent discovery on several servers uses `INSERT … ON CONFLICT` under one lock per bundle and retries lost races.

Consumer rows may appear up to ~25 s after a bundle reports healthy; a tool reading the catalog right after a rollout should wait.

## Regions as contexts

When data must stay in its region, publish regional events with the region as their [context](../../evento-framework/eventobundle/context.md) and let each cell consume only its regions:

```java
EventoBundle.Builder.builder()
    .setComponentContexts(OrderProjector.class, "EUROPA", "AFRICA", "ALL")
```

`setComponentContexts` starts **one consumer engine per context** (own consumer id, checkpoint and lock). Use **one generic component and configuration-driven contexts**, not one class per region. `*` (`Context.WILDCARD`) is the only wildcard and reads every context; `"ALL"` is an ordinary context name, a natural choice for events that every region needs (a price list), consumed by one global lane. `_` and `%` in context names are matched literally (`SUD_AMERICA` does not match `SUDXAMERICA`).

## Sizing and limits

* Put the event-store primary in the cell with the most writes: every append serializes on a global lock reached over the WAN, so a remote command costs several round trips (p50 ≈ 0.7 s at 80 ms RTT, ≈ 1.2 s at 150 ms).
* Consumer lanes have no cell affinity: the instance holding a lane can be in a remote cell and write over the WAN.
* The GUI dashboard and consumer administration show the view of the server you connect to.
