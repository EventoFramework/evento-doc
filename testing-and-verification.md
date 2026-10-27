---
description: The tests every Evento 3 release goes through, and what they showed
---

# How Evento Is Tested

A framework that promises exactly-once commands, failover and consumers that never skip an event has to prove it under failure, not only in the happy path. This is what Evento 3 went through before release.

## Automated test suite

**Over 1,000 automated tests**, run on every change by continuous integration:

* unit and integration tests over **real TCP connections**, not mocks, between bundles and servers;
* the event store, the catalog and the consumer state store against **PostgreSQL 16 and 17 and MySQL 8.4**, in containers;
* multi-server tests: several complete servers on one database, bundles moving between them, stale sessions, concurrent discoveries;
* the Spring Boot starter on Boot 4 and 3.5;
* a containerised server started from the image that is released.

## Chaos lab: three regions, nineteen scenarios

A lab reproduces a deployment across three continents: three servers (Europe, Americas, Asia-Pacific), one PostgreSQL event store with replicas, simulated WAN latency between regions, every bundle replicated, and a load generator placing orders in seven regions. Nineteen scenarios break it on purpose:

| Scenario | What is done to the cluster |
|---|---|
| Baseline | steady load across all regions |
| Kill a handler replica / kill a server | processes killed mid-load |
| Server returns | a server killed and restarted, or frozen past its timeouts and resumed |
| Region partition | one region cut off the network, then healed |
| Event-store and application database failover | the primary database replaced mid-load |
| Concurrent commands on one aggregate | conflicting writes from several regions at once |
| WAN latency sweep | latency raised step by step |
| Cold start | three servers starting together on an empty database |
| Wrong broker, clock skew, retry storm | misconfiguration, a clock 40 s off, clients retrying aggressively |
| Context routing, context isolation, global fan-out | regional and global consumers, lanes moving between replicas |

After every scenario the lab checks the invariants that matter:

* **no acknowledged command lost**, and nothing stored that was not acknowledged;
* **no duplicate** events or side effects (a payment is never taken twice);
* **no forked aggregate**;
* each region's read model holds **only its own data**, and the global one holds **all of it**;
* the read models **converge** to the event store;
* the catalog lists **every live bundle, handler and consumer**.

On Evento 3 every invariant holds in every scenario. During a region partition the other regions keep acknowledging **100 %** of their commands.

## Rolling upgrades

The same lab runs servers and bundles of different versions together, in every order, and upgrades a running cluster one server and one bundle at a time on a database that already holds data. Every step keeps the invariants above.

## Highly available consumers

One consumer per context, each in **three replicas** with their own connection pool, on one database for locks and checkpoints. While events of three contexts stream in, the replica that holds each context's lane is killed, twice. Every event of every context is applied **exactly once and in order**, and no event crosses into another context.

## Real applications

Before release, Evento 3 ran the full test suites of two production systems built on it: a marketplace (1,385 tests, and a clean start on an empty database with its data seeders) and a manufacturing-execution system (153 end-to-end tests across eleven services).

## Benchmarks

Tests say that nothing breaks; benchmarks say what it costs. Each number below was measured on Evento 3 and can be reproduced from the repository.

**Write throughput.** One server on a 4-core machine with PostgreSQL (CPES, the default event-store mode, with group commit) stores about **3,900 commands a second**, each creating a new aggregate, with 128 commands in flight and a p99 latency of about 60 ms. APES, the deprecated mode, is no faster on one server.

**Command latency, phase by phase.** Every aggregate command is timed by the server from its arrival to its reply (queue, lock, history, handler, append, reply), and the same timers are exported as metrics in production.

| Where the command runs | p50 | p95 | p99 |
|---|---:|---:|---:|
| One machine, existing aggregate, 1 command in flight | 7.2 ms | 10.6 ms | 18.7 ms |
| One machine, existing aggregate, 8 in flight | 19.3 ms | 22.2 ms | 27.3 ms |
| Lab, Europe (event-store primary in the region) | 97 ms | 175 ms | 249 ms |
| Lab, Americas (80 ms from the primary) | 595 ms | 752 ms | 821 ms |
| Lab, Asia-Pacific (150 ms from the primary) | 1,008 ms | 1,234 ms | 1,459 ms |

On one machine the time goes mostly to the commit of the append. Across regions it is the number of round trips to the event-store primary times the distance, with a synchronous replica in another region: which is why a write-heavy context belongs in the region of its primary (see [Cells and Locality](evento-server/evento-server-cluster/cells-and-locality.md)).

**Synchronous replication across availability zones.** With a synchronous standby 10 ms away, every commit waits for the standby, and under CPES the global append lock waits with it. Measured, this is the one case where APES stores more commands a second, and it needs several servers, where APES is unsafe for consumers: hence CPES as the default and APES deprecated (see [Event Store Modes](evento-server/setup-evento-server/evento-event-store-modes-apes-and-cpes.md)).

**What a query answer costs the server**, for a single 64 MiB answer:

| Mode | Caller time | Server heap kept afterwards | Server CPU |
|---|---:|---:|---:|
| Classic answer | 602 ms | ~0 | 281 ms |
| Stream through the server | 243 ms | ~0 | 547 ms |
| Direct stream between bundles | 153 ms | 0 | 0 |

The server keeps no query answer once it is delivered, and streaming carries a large answer in less than half the time (see [Streaming and Paged Queries](evento-framework/component/projection/streaming-and-paged-queries.md)).

**Measured in the chaos lab too:** the WAN latency sweep raises the latency between regions step by step and checks that every invariant still holds, and the watermark scenario measures what keeping consumers aligned costs a server under load.

## Reproduce it

Everything above lives in the [framework repository](https://github.com/EventoFramework/evento-framework): the test suites, the chaos lab (`evento-lab-cluster`, with the reports of each run under `results/`), the microservices lab (`evento-lab-microservices`) and the benchmarks (`QueryPathBenchmarkIT` and `CommandLatencyBenchmarkIT` in `evento-server`, run with `EVENTO_RUN_BENCH=true`, and the write-throughput harness under `benchmarks/`).
