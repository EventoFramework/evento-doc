---
description: Rollout order and behaviour changes for 3.0 (query path, payload versioning, aggregate commands, APES deprecation, licence)
---

# Upgrading to 3.0

3.0 changes the query path (streamed, paged and locally answered queries, read-your-writes, compression, bounded server memory), adds [payload versioning](../../evento-framework/payload-and-messages/payload-versioning.md) fences aggregate appends in the database, runs aggregate commands without the lock and with group commit, and deprecates APES. There is **one additive schema change** (section 6), and the server now migrates its schema with Flyway (section 7). Wire changes are additive and negotiated in the handshake (capabilities `stream:1`, `revision:1` and `events:1`): 2.5 and 3.0 bundles and servers interoperate in any mix, with the exceptions below.

## 0. The server now refuses to start unhardened

3.0 is a major release, and changes one default: `evento.server.security.profile` is `prod`. A server that has no bus auth token, no bus TLS, no payload allowlist, the shipped passwords or `*` as CORS origin **does not start** and lists what is missing ([Security](../setup-evento-server/security.md)). Fix the list, or set `EVENTO_SERVER_SECURITY_PROFILE=dev` where that is acceptable (development, tests, demos). A deployment that runs the image as `eventoframework/evento-server:latest` gets 3.0, and this check, on its next pull: pin a version and upgrade on purpose. Everything else below is backward compatible: 2.5 and 3.0 bundles and servers interoperate.

## 1. Servers first, then the bundles

Upgrade the servers, then roll the bundles at your own pace. Servers can be upgraded one at a time.

{% hint style="warning" %}
**Three features need 3.0 servers**, and a 3.0 bundle refuses to use them through a 2.5 server (the error says so), rather than lose data:

* a class annotated with `@Revision` (a 2.5 server would store it as revision 0);
* an aggregate command handler that returns `DomainEvents` (a 2.5 server would store only the last event);
* `@PersonalData` fields (a 2.5 server cannot hand out the keys).

Deploy them only once every server is on 3.0.
{% endhint %}

{% hint style="info" %}
**About `@Revision`, in detail.** A 2.5 server re-encodes payload envelopes without their revision, so a 3.0 bundle refuses to send or store a revised payload through it (the error says so). Deploy the first `@Revision` only once every server is on 3.0. Unrevised payloads, the default, flow through any server.
{% endhint %}

## 2. Rebuild the bundles: dependencies and Java

The client libraries (`evento-bundle`, `evento-common`, the transports, the consumer state store) changed what they bring into your application:

* **Java 21 or later** is enough for them (the server needs 25).
* **Logging goes through SLF4J only.** The libraries no longer bring Log4j: an application that relied on it (directly, or through a `log4j2.xml` it never declared a dependency for) must add its own SLF4J backend (Logback, `log4j-slf4j2-impl`...) or it logs nothing. Spring Boot applications already have one.
* **`hibernate-validator` is no longer pulled in** by `evento-bundle`. If your code uses `jakarta.validation` through it, declare it yourself, or the build fails.
* A payload that cannot be serialized now **fails the send** with an `IllegalArgumentException` that names the class; 2.5 logged the error and sent a null payload.
* **Size the consumer state-store pool for the consumers.** A `JdbcConsumerLock` keeps a consumer's lock, and its connection, between fetch cycles, so that a lane stays on one replica: give the pool of the consumer state store **one connection per consumer of the instance plus a few** for the checkpoint writes (a bundle with 17 projectors: 24). A smaller pool still works: the locks then take at most `max - max(2, max / 4)` connections, the consumers take turns as in 2.5, and the bundle logs `event=consumer_lock_pool_bound` once. The bound is read from a pool that tells its maximum size (HikariCP); with another pool pass it to `new JdbcConsumerLock(dataSource, dialect, affinity, maxHeld)`.

## 3. Queries are "straight"

A 3.0 server routes a query declared by a 3.0 handler bundle straight: its answer is not kept for exactly-once replays and not buffered while the caller reconnects (queries are idempotent reads; keeping answers is what filled the server's heap with large results). A 3.0 caller that loses its session while a query is in flight **asks it again** on its next session, on whatever server. A 2.5 caller in the same situation now waits for its timeout instead of getting the buffered answer: **upgrade callers along with the handler bundles**.

Event fetches of the consumers are asked again after a lost session in the same way.

## 4. Review the server's memory bounds

What the server keeps for commands is now bounded in bytes as well as in entries. The defaults fit most deployments; see `evento.server.bus.dedup.*`, `evento.server.bus.reconnect-buffer.max-bytes` and `evento.server.bus.compression.threshold-bytes` in [Advanced Options](../setup-evento-server/advanced-options.md).

## 5. Adopt the new features where they pay off

Nothing has to change in the bundles' code. Then, where useful:

* `QueryGateway.stream(...)`, `Streamed<View>`, `Page<View>` and direct streams for large answers: [Streamed and Paged Queries](../../evento-framework/component/projection/streaming-and-paged-queries.md).
* `CommandGateway.sendTracked(...)` and `QueryOptions.after(token)` / `readYourWrites()`: [Read Your Writes](../../evento-framework/component/projection/read-your-writes.md).
* `@Revision` and upcasters when a payload class must change shape or name: [Payload Versioning and Upcasting](../../evento-framework/payload-and-messages/payload-versioning.md).
* Several events from one aggregate command (`DomainEvents`): [@AggregateCommandHandler](../../evento-framework/component/aggregate/aggregatecommandhandler.md#returning-several-events).
* Personal data and the right to erasure (`@PersonalData`): [Personal Data](../../evento-framework/personal-data.md).
* The Spring Boot starter, OpenTelemetry tracing and the test fixtures (`evento-test`, `EventoTestBroker`, `EventoServerContainer`): [Spring Boot Starter](../../evento-framework/eventobundle/spring-boot-starter.md), [Testing with Fixtures](../../evento-framework/testing-with-fixtures.md).
* A retention for idempotency keys (`evento.es.idempotency.retention`), off by default: [Advanced Options](../setup-evento-server/advanced-options.md).

A bundle now answers the queries it handles itself, without the server (`setLocalQueryShortCircuit(false)` to turn it off). Tracing, metrics and the GUI see these queries as before.

**Consumers at the head no longer poll.** A 3.0 server tells its 3.0 bundles when the event store has grown, and which events were appended (`evento:events-appended`, every `evento.es.head.poll.ms`, 50 ms by default; 0 turns it off): a consumer at the head waits for a notice about an event it handles, up to its fetch delay (`setSssFetchDelay`, 1 s by default) as a safety net. In 2.5 an idle consumer fetched again every few milliseconds, which at rest kept the event store busy (on a hundred consumers, hundreds of queries a second) and under load queued the useful fetches behind the empty ones. With a 2.5 server, or for a 2.5 bundle, the consumers poll as before. An event whose stored name no handler declares (renamed through an upcaster) reaches its consumer at the fetch delay.

Code that asserts the exact capability set of a bundle's handshake must expect `stream:1`, `revision:1`, `events:1` and `head:1`.

Removing a bundle from the catalog in the console (`DELETE /api/bundle/{id}`) now needs the `ADMIN` role.

## 6. The aggregate fence (schema change)

Every event of an aggregate command now carries the aggregate's version, in a new column `es__events.aggregate_seq` (1, 2, 3... per aggregate) under a unique index on `(aggregate_id, aggregate_seq)`. The server reads the version together with the aggregate's events and stores the new event as the next version, so **two commands that decided from the same state can no longer both store their event**: the database refuses the second one. Before 3.0 this could happen when a server lost the aggregate lock (a failover, a dead database session) and, without any fault, for a command whose `getLockId()` returns `null`.

* **With `spring.sql.init.mode=always`** (the default) the first 3.0 server adds the column and the index at boot, without blocking appends: the column is a catalog-only change and the index is built `CONCURRENTLY`. Existing events keep an empty version and are outside the index.
* **With a schema managed outside the server** apply `classpath:db/upgrade/es-events-aggregate-seq.sql` (in `evento-server.jar`), outside a transaction block. Until then the server logs `event=aggregate_fence_unsupported` and appends as 2.5 did; it notices the script within a minute, without a restart.
* **The fence holds once every server runs 3.0**: a 2.5 server appends without a version.

{% hint style="info" %}
**Commands without a lock no longer fork the aggregate.** If a `DomainCommand` overrides `getLockId()` to return `null`, two concurrent commands on one aggregate used to both succeed from the same state. Now the second one loses the fence, nothing of it is stored, and the server runs it again on the new state under the aggregate lock: its caller gets the answer computed on the current state, which may be a refusal by the domain. `AggregateConflictException` is answered only when 5 runs within the deadline all lost (`event=aggregate_fence_conflict`, `evento.server.commands.fence.conflicts`).
{% endhint %}

## 7. The schema is migrated by Flyway

With `spring.sql.init.mode=always` (the default) the server keeps its schema with Flyway: the first 3.0 server creates the history table `evento_es_schema_history`, takes an existing database in at version 0 and runs the migrations V1-V7, which find what is already there and add what is missing (section 6 included), without blocking appends. The database user of the server needs the right to create that table. Servers starting together still migrate once. Later versions add migrations; there is nothing to do by hand. With `spring.sql.init.mode=never` nothing changes: the server touches no schema.

## 8. Aggregate commands run without the lock

With the fence in place (section 6) the server no longer takes the aggregate lock for every command (`evento.server.commands.optimistic=true`): it loads the story, runs the handler and stores the event, and the fence refuses the event if another command got there first. That command then runs again on the new story, under the lock. An aggregate that is contended (another command for it in flight on the server, or a refused event on it in the last 2 s) takes the lock from the start, so a hot aggregate still queues instead of losing races. The lock cost three round trips to the database per command and a lock connection for the whole run; without it one server stores several times more commands a second.

* **Aggregate handlers must be pure**: compute the event from the story and the command, with no side effects (the documented contract, now relied upon), since a handler can run more than once for one command. Only one event is ever stored.
* A duplicate of a command sent with an idempotency key can run the handler on another server while the first is in flight; still only one event is stored.
* `evento.server.commands.optimistic=false` takes the lock for every command, as in 2.5. A command whose `getLockId()` names another key than its aggregate keeps that lock.
* Metrics: `evento.server.commands.optimistic`, `evento.server.commands.fence.retries`.

## 9. Capacity defaults

* **Group commit.** Appends that arrive together are written in one statement and one commit (`evento.es.append.batch.writers`, `evento.es.append.batch.max-size`). Under CPES the batch's events get consecutive numbers, so the commit order is still the sequence order.
* **`evento.server.bus.business-executor-max-size` is `cores × 32`** (was `cores × 8`). If you set it explicitly, review it.
* **Lock waits queue in PostgreSQL.** A command waiting for an aggregate another server holds now waits in PostgreSQL's queue, on a connection of the lock pool (at most half of it; the rest poll as before), so servers take turns on a hot aggregate instead of one server keeping it. Size `evento.lock.pool.maximum-size` for the locks held at once plus the contended aggregates waiting.

## 10. APES is deprecated

On one server CPES is now as fast as APES, and with several servers APES consumers can skip events. A server started with `evento.es.mode=APES` logs `event=es_mode_deprecated`. To move an APES store to CPES, stop every server and start them with `evento.es.mode=CPES`: the sequence goes on above the newest APES id. See [Event Store Modes](../setup-evento-server/evento-event-store-modes-apes-and-cpes.md).

## 11. Licence: everything public

The server and the web console move from AGPL-3.0 (or commercial) to **Apache-2.0 with the Commons Clause**, and single sign-on and the audit trail, until now a separate commercial distribution, are part of the server: the same jar and image for everyone. Running, changing and using Evento, also commercially, needs no licence; selling Evento itself (hosting it for others, reselling it, consulting or training about it) needs a written authorisation. The client libraries stay Apache-2.0. See [Licensing](../../licensing.md).
