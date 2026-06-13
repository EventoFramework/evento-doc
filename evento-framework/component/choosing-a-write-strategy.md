---
description: A core design choice — reads vs writes, and how to pick a write strategy per data flow
---

# Choosing a Write Strategy: Reads vs Writes

Before mapping a data flow onto Evento components, it pays to understand a fundamental design choice baked into the framework. Evento — and the RECQ architecture it implements — is **optimised for read-heavy systems**, where reads vastly outnumber writes (writes ≪ reads). Most line-of-business and domain systems fit this shape: an order is placed once but its status is read many times; a catalog item is updated rarely but queried constantly.

This chapter explains the **default CQRS write path**, why it is the right tool when the write side must enforce invariants, and — just as importantly — when you should deliberately **bypass it** in favour of a `@Service` that writes directly to its datastore. Choosing the right strategy per data flow is not an optimisation you bolt on later: it determines your throughput ceiling, your ordering guarantees, and how the system behaves after a crash.

#### The Default Path: Command → Aggregate → Event → Projector → Projection

In the canonical Evento flow, a write travels through a well-defined pipeline:

1. **Command** — an instruction to change state is sent to the write side.
2. **`@Aggregate`** — the consistency-enforced write side. An aggregate is the single unit of consistency for its slice of the domain. Within a [context](../eventobundle/context.md), an aggregate instance is consumed **single-active** (one active consumer at a time), which gives you **ordered**, **exactly-once**, **invariant-preserving** command handling. This is what lets you guarantee rules such as *"never oversell stock"* or *"no double-booking"* — the aggregate sees a consistent, serialised view of its own history before it decides whether a command is allowed.
3. **Event** — the aggregate emits immutable domain events recording what happened. These events are the durable source of truth, persisted in the event store.
4. **`@Projector`** — projectors subscribe to those events and materialise them into…
5. **`@Projection`** — a denormalised, query-optimised read model that can be **horizontally scaled** independently of the write side.

This separation is precisely what makes a read-heavy system fast: the write side stays small and strongly consistent, while the read side can be replicated and shaped for exactly the queries your application makes.

#### The Read Model Is Eventually Consistent

The read model is built **asynchronously**. Projectors materialise events after they are committed on the write side, so there is an inherent **read-after-write lag**: immediately after a command succeeds, a query against the projection may not yet reflect it. Under a **write burst**, projectors can fall behind and the read side lags further until it catches up.

{% hint style="info" %}
This is by design. In a read-heavy system the small, bounded staleness of the read model is an excellent trade for the horizontal read scalability and the strong write-side invariants you get in return.
{% endhint %}

The same property explains projector behaviour **after a crash or restart**. Projectors **rebuild by replaying** events from the store (optionally accelerated by aggregate snapshots — see [@Aggregate](aggregate/README.md)). The time taken to catch up is a **performance characteristic of the eventually-consistent read side, not a durability problem**:

* The **durable truth** lives in the event store and your write-side databases. It survives the crash unchanged.
* The **read model is reconstructed** from that truth. A projection that was lost or stale is simply re-materialised by replay.

In other words, a slow catch-up means *queries are briefly stale*, never that *data is lost*.

This design is ideal when reads dominate **and** the write side genuinely needs invariants. If your domain has rules that must hold no matter what — uniqueness, non-negative balances, capacity limits — the aggregate's ordered, exactly-once consumption is exactly the guarantee you want.

#### When the Default Path Is the Wrong Tool: High-Throughput Writes

The aggregate pipeline buys consistency by **serialising writes per context**. That is a feature when you need invariants, but it becomes a bottleneck — plus the added projector catch-up — when a data flow has:

* **high write volume**, and
* **no cross-entity consistency invariant** — the write does not need ordering, exactly-once semantics, or aggregate-enforced rules.

Forcing such a flow through aggregate → event → projector is the wrong tool. You pay for serialisation and materialisation you do not need.

For these flows, use a **`@Service` that writes directly to its datastore**, bypassing the aggregate/event/projector pipeline entirely. A service is free to run with **maximum parallelism**, so it can absorb a high concurrent write load that an aggregate would serialise.

{% hint style="info" %}
**Industrial precedent.** A large industrial MES/MOM (Manufacturing Execution / Operations Management) system ingests **all of its IoT telemetry at the `@Service` level**, writing directly to the datastore. Telemetry arrives at very high throughput, and its consistency is **not an application consistency constraint** — there is no invariant like "reading N must come after reading N−1" that the application must enforce. Routing that firehose through aggregates would needlessly serialise it; a direct-write service handles it with the parallelism the workload demands.
{% endhint %}

#### Decision Rule

Apply this per data flow, not once for the whole system:

* **Needs write-side invariants / ordered, exactly-once consistency** → use an **`@Aggregate`** (with `@Projector` + `@Projection` for the read side). Examples: stock that must never oversell, bookings that must not collide, balances that must not go negative.
* **High write throughput, no cross-entity invariant, loose/eventual consistency acceptable** → use a **`@Service`** that writes directly to its datastore for maximum parallelism. Examples: IoT/sensor telemetry, high-volume logging or metrics, append-only ingestion where order is irrelevant.
* **Mixed systems** — most real systems — combine both: **aggregates for the consistency-critical core**, and **services for high-volume peripheral writes**. The two coexist in the same application and even the same context.

#### Operational Implication

Make this choice **up front**, per flow. The write strategy you pick is not a tunable knob you can flip later without consequence — it determines:

* **throughput** — how much concurrent write load the flow can absorb;
* **ordering guarantees** — whether commands are serialised and exactly-once, or processed in parallel with no ordering promise;
* **crash-recovery behaviour** — whether recovery means *replaying events to rebuild a read model* (aggregate path) or *the data simply already being in the datastore* (direct-write service).

Get the classification right when you design the flow, and Evento gives you both a strongly consistent core and a read side that scales — without paying for consistency you do not need.
