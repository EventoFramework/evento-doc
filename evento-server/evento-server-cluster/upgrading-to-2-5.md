---
description: Rollout order, first-boot schema migrations and connection sizing for 2.5.x
---

# Upgrading to 2.5

Wire changes in 2.5 are additive: 2.4 bundles work against 2.5 servers unchanged, and 2.5 bundles run against 2.4 servers (without exactly-once and without probe-gated fail-back). The **database schema** is migrated on the first boot of a 2.5 server, which drives the rollout order. Patch releases mix freely with 2.5.0: 2.5.1 updates dependencies only, and 2.5.2 fixes a race in which a reply written just before its sender closed the session (the end of a fail-back drain) could be lost. **Prefer 2.5.2.**

## 1. Upgrade every server together, then the bundles

Stop all 2.4 servers that share the database, start the 2.5 servers, then roll the bundles at your own pace.

The first 2.5 server to boot re-keys the component catalog; a 2.4 server still running against the same database fails its catalog writes from then on (routing keeps working, discovery and consumer registration do not). Mixed servers also weaken exactly-once: a keyed retry that lands on a 2.4 server runs unkeyed.

## 2. Schema migrations on the first boot

With `spring.sql.init.mode=always` (the shipped value) the server migrates the schema at boot, serialized across servers by a PostgreSQL advisory lock; every step is idempotent and a re-boot is a no-op.

* **`es__events` primary key.** A full-table duplicate check, then `CREATE UNIQUE INDEX CONCURRENTLY` (appends continue), then an instant `ACCESS EXCLUSIVE` swap under `lock_timeout` 3 s, retried. **On a large event store the first server's boot lasts as long as that scan plus the index build** (other servers wait on the schema lock). To keep it out of the boot, apply `db/upgrade/es-events-primary-key.sql` (inside `evento-server.jar`) by hand beforehand. Duplicate sequence numbers fail the boot with their count; resolve them, or boot with `evento.es.schema.enforce-primary-key=false`.
* **Idempotency keys.** Nullable columns `es__events.idempotency_key` / `idempotency_command`, a partial unique index built `CONCURRENTLY` (it covers only keyed rows, so existing data cannot violate it), and the table `es__idempotency_claims`.
* **Catalog re-key.** `core__component` is keyed per bundle (`bundle_id:component_name`) and `core__handler` / `core__consumer` move to `component_id`: one transaction over a few hundred rows.
* **Presence.** New table `core__bundle_instance`.

With the schema managed outside the server (`spring.sql.init.mode=never`) nothing is changed: apply `db/upgrade/n1-component-id.sql` (required — the server refuses to boot over the old catalog), `es-events-primary-key.sql` and `es-events-idempotency-key.sql` (optional, warned about) yourself.

## 3. Size the connections

Each server now runs an application pool of 20 (5 idle; it was Hikari's default 10) plus a dedicated lock pool of 10. Peak **30 per server**: three servers fit PostgreSQL's default `max_connections=100`. With more servers, or other clients on the same database, raise `max_connections` or lower the pools first.

Lock waits are now bounded (`evento.lock.acquire.timeout.ms`, 60 s) and throw `LockAcquisitionTimeoutException` / `LockLostException` instead of hanging.

## 4. Set the new server properties

* `evento.cluster.name` — per deployment (the shipped value is the same everywhere).
* `evento.cluster.node.server.id` — unique per server.
* Optional: `evento.server.bus.pick-strategy=locality-preferred` with bundle zones; `evento.server.presence.*`.

See [Cluster Configuration](cluster-configuration.md).

## 5. Review the bundles

* **Every configured address is used now** (2.4 ignored addresses 2..n) and the bundle **fails back** to the first one by default: list the bundle's local server first.
* **Commands sent from sagas, projectors and observers carry derived idempotency keys**, so a redelivered event no longer re-executes them. Rewinding a consumer answers its re-sent commands as replays; rewind under a new consumer id to run them again.
* The **service outcome store** is opt-in: set it on service bundles that need exactly-once (`setServiceCommandOutcomeStore`), shared by all their instances.
* **Commands past their caller's deadline are no longer executed.** Callers that relied on a timed-out command still being applied must retry it — with an idempotency key.
* `Context.ALL` is deprecated in favour of `Context.WILDCARD` (both are `"*"`).

## 6. Runtime requirements

* **PostgreSQL 12** or later.
* **JDK 25.0.3** or later: 25.0.1 and 25.0.2 carry JDK-8370887 (virtual-thread timed waits can stall for ~20 s); bundles and the server log `event=jdk_virtual_thread_timer_bug` at startup on those builds.

The full list of changes is in the [CHANGELOG](https://github.com/EventoFramework/evento-framework/blob/main/CHANGELOG.md).
