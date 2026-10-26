---
description: Everything Evento 3 gives you, in one page
---

# Evento 3

**Evento 3 is available.** It is the complete toolkit to build RECQ systems in Java: seven component types to write your domain with, a server that routes and stores everything they exchange, a console that turns your code into a living map of the system, and a cluster mode that runs it from one site to three continents. Every feature is public: the client libraries under Apache-2.0, the server and console under Apache-2.0 with the Commons Clause ([Licensing](licensing.md)).

## Write your domain

* **Seven RECQ components**, each an annotated Java class: [Aggregates](evento-framework/component/aggregate/README.md), [Services](evento-framework/component/service/README.md), [Projectors](evento-framework/component/projector/README.md), [Projections](evento-framework/component/projection/README.md), [Sagas](evento-framework/component/saga/README.md), [Observers](evento-framework/component/observer.md) and [Invokers](evento-framework/component/invoker.md). Bundles announce their components to the server on their own: no deployment descriptors.
* **Commands, events and queries** as plain payload classes, with [versioning and upcasting](evento-framework/payload-and-messages/payload-versioning.md): a class can change shape or name and the history written with the old one is still read.
* **Several events from one command**, stored atomically ([returning several events](evento-framework/component/aggregate/aggregatecommandhandler.md#returning-several-events)).
* **Any Java stack**: plain Java, Spring, Micronaut or Quarkus; a [Spring Boot starter](evento-framework/eventobundle/spring-boot-starter.md) for Boot 4 and 3.5. Client libraries need Java 21; the server runs on Java 25 with virtual threads.

## Correct under failure

* **Exactly-once commands**: idempotency keys make a retry safe on whichever server it lands, and sagas, projectors and observers derive theirs automatically ([Exactly-once Commands](evento-server/evento-server-cluster/exactly-once-commands.md)).
* **No forked aggregates**: every event carries its aggregate's version under a unique index, so two commands that decided from the same state can never both be stored; commands run without a lock and retry on the new state when they lose.
* **Consumers you can trust**: projector, saga and observer progress on [PostgreSQL or MySQL](evento-framework/eventobundle/consumerstatestore/README.md), [dead event queues](evento-framework/dead-event-queues.md), [parallel consumption](evento-framework/eventobundle/parallel-consumers.md) with per-aggregate ordering when you need it.
* **Consumers that wait instead of poll**: the server tells the bundles when events of the kinds they handle arrive; an idle system costs the event store almost nothing.

## Run it as a cluster

* **Several servers, one PostgreSQL event store**: from a hot standby next to your server to a cell per region ([Evento Server Cluster](evento-server/evento-server-cluster/README.md)).
* **Failover and fail-back**: bundles move to another server when theirs dies and come back on their own when it is healthy again ([Bundle Failover and Fail-back](evento-server/evento-server-cluster/bundle-failover-and-failback.md)).
* **Cells and locality**: requests are answered close to the caller ([Cells and Locality](evento-server/evento-server-cluster/cells-and-locality.md)).
* **Highly available consumers**: run each consumer, per context, in as many replicas as you like; one replica holds the lane and another takes over when it goes, without losing or repeating an event.
* **Correctness lives in the database**: servers never call one another, so adding one is just starting it.

## Query at any size

* **Streamed and paged answers** with flow control, even directly from bundle to bundle; a bundle answers its own queries in process ([Streamed and Paged Queries](evento-framework/component/projection/streaming-and-paged-queries.md)).
* **Read your writes**: a query can wait until the projections reflect a command ([Read Your Writes](evento-framework/component/projection/read-your-writes.md)).

## Secure and compliant

* **Secure by default**: in production the server requires a bus token, TLS, a payload allowlist, real passwords and explicit CORS origins ([Security](evento-server/setup-evento-server/security.md)).
* **Single sign-on and audit trail** for the console ([GUI Auth](evento-gui/gui-auth.md)).
* **Personal data and the right to erasure**: personal fields are encrypted per data subject, and deleting the subject's key erases them from the whole history ([Personal Data](evento-framework/personal-data.md)).
* **Multi-tenancy** patterns ([Multi-Tenancy](evento-framework/multi-tenancy.md)).

## See and measure

* **A console generated from your code**: catalog of payloads, components and bundles, flows, application graph, what-if performance analysis ([Evento GUI](evento-gui/explore-recq-systems-visually.md)).
* **OpenTelemetry tracing and Prometheus metrics** ([OpenTelemetry](evento-framework/eventobundle/tracingagend-and-track/opentelemetry.md)).

## Test it

* **Fixtures, an in-process broker and a containerised server** to test components alone or a whole system ([Testing with Fixtures](evento-framework/testing-with-fixtures.md)).

And Evento itself is tested hard: see [How Evento Is Tested](testing-and-verification.md).
