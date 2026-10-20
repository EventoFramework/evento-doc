# Evento Event Store Modes: APES and CPES

The event store numbers every event it stores; consumers read events in that order and remember the last number they processed. `evento.es.mode` chooses how the numbers are made. **CPES is the default and the mode to use. APES is deprecated since 3.0.**

#### CPES Mode (default)

CPES (Consistent and Partitionable Event Store) takes consecutive numbers from one PostgreSQL sequence, under a global advisory lock held until the commit. The order of the numbers is therefore the order of the commits, on any number of servers: a consumer reads every event as soon as it is committed, with no delay and without ever skipping one.

Since 3.0 appends that arrive together are written in one statement and one transaction (group commit): the batch takes the lock once and its events get consecutive numbers, so the lock no longer limits throughput the way one commit per event did. On a 4-core machine one server stores about 3,900 commands a second (one new aggregate each, 128 in flight, p99 about 60 ms).

#### APES Mode (deprecated)

APES (Available and Partitionable Event Store) numbers events with [Snowflake ids](https://en.wikipedia.org/wiki/Snowflake\_ID) taken by each server from its own clock, and commits in parallel. Because an id is taken before its commit, a consumer cannot read up to the newest id it sees: it reads only ids older than `evento.es.fetch.delay` (69 ms), and an event whose commit comes later than that after its id was taken is **skipped** by consumers that already read past it. With several servers the ids also come from several clocks and from node ids derived from the MAC address.

#### Why APES is deprecated

Measured in 3.0 (benchmarks B1 and B2 in the Evento repository, `benchmarks/axon-comparison`):

* **On one server APES is no faster.** With group commit CPES stores as many commands a second (3,907 against 3,852 at 128 in flight) and has the better tail latency when commands share aggregates.
* **APES is faster only with synchronous replication across availability zones.** PostgreSQL releases a transaction's locks only after the synchronous standby has confirmed it, so under CPES every batch holds the global lock for the standby's round trip too. With 10 ms between zones APES stored 2 to 3 times more commands a second at low concurrency.
* **That case needs several servers, where APES is unsafe** for consumers, for the reasons above.

Where APES is safe it brings nothing, and where it brings something it is not safe. It still works; it will be removed in a later major version. A server started in APES logs `event=es_mode_deprecated`.

#### Moving an APES store to CPES

1. Stop **every** server.
2. Start them with `evento.es.mode=CPES`.

The first CPES server finds the sequence behind the newest stored number and moves it above (under the global lock, logged `event=es_mode_switched`). New events then sort after every APES event, and consumer checkpoints stay valid. On a store CPES has always numbered nothing happens.

{% hint style="warning" %}
Never run APES and CPES servers on the same store: an APES server takes ids millions above the numbers CPES gives, and a CPES consumer that read one of them skips the CPES events committed below it. If the newest id is less than a minute old at the switch, the server logs `event=es_mode_switch_while_apes_active` (ERROR): check that no APES server is still running.
{% endhint %}
