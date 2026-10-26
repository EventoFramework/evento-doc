---
description: The tests every Evento 3 release goes through, and what they showed
---

# How Evento Is Tested

A framework that promises exactly-once commands, failover and consumers that never skip an event has to prove it under failure, not only in the happy path. This is what Evento 3 went through before release.

## Automated test suite

**1,130 automated tests**, run on every change by continuous integration:

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

The same lab runs servers and bundles of the previous release line and of Evento 3 together, in every order, and upgrades a running cluster one server and one bundle at a time on a database created by the previous release. Every step keeps the invariants above.

## Highly available consumers

One consumer per context, each in **three replicas** with their own connection pool, on one database for locks and checkpoints. While events of three contexts stream in, the replica that holds each context's lane is killed, twice. Every event of every context is applied **exactly once and in order**, and no event crosses into another context.

## Real applications

Before release, Evento 3 ran the full test suites of two production systems built on it: a marketplace (1,382 tests, and a clean start on an empty database with its data seeders) and a manufacturing-execution system (153 end-to-end tests across eleven services, all passing on the first run).

## Reproduce it

Everything above lives in the [framework repository](https://github.com/EventoFramework/evento-framework): the test suites, the chaos lab (`evento-lab-cluster`, with the reports of each run under `results/`) and the microservices lab (`evento-lab-microservices`).
