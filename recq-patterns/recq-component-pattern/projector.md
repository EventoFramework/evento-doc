---
description: >-
  Component that implements the Query Model of the CQRS pattern, but only deals
  with the writing part of the local model.
---

# Projector

<figure><img src="../../.gitbook/assets/image (42).png" alt=""><figcaption><p>RECQ Projector Big Picture</p></figcaption></figure>

Projectors are specialized components dedicated to processing events published to the System State Store (SSS) and transforming them into a format optimized for efficient querying. This processed data forms the foundation of your application's read models.

**The `EventHandler` Method: The Heart of Projection Logic**

Projectors expose a single method "on" – the `EventHandler`. This method acts as the workhorse, taking an individual Event (state change) as input. Here's what happens within the `EventHandler`:

* **Event Processing:** The Projector analyzes the received Event and utilizes it to update its internal representation of the domain model. This internal model reflects the current state of the data relevant to the Projector's purpose.

**No Return, All Transformation:**

Unlike command handlers in Aggregates, Projectors do not return any value from their `EventHandler` method. Their primary focus lies on transforming the event data and integrating it into the internal read model.

<figure><img src="../../.gitbook/assets/image (37).png" alt=""><figcaption><p>Projector Structure</p></figcaption></figure>

**Ensuring Consistency, One Event at a Time**

Projectors prioritize consistency over raw processing speed. They process events in a strictly sequential manner, ensuring that the internal read model reflects the state changes in the correct order.

**Single Active Instance per Context**

To maintain this ordering guarantee, only one Projector instance is *active* at a time **per context** — a named partition of the event stream that bounds both where and in what order events are applied. Other instances stand by as failover: if the active one dies, a replica takes over from the last recorded checkpoint, so replication buys availability. Throughput, on the other hand, scales *horizontally by partitioning*: the event stream can be split into multiple independent contexts, and each context is projected concurrently by its own active instance. A Projector is therefore not a system-wide singleton — it is single-active within each context, and parallel across contexts.

**Internal State and Shared Consumer State Stores**

Projectors maintain an internal state that tracks their progress in consuming events from the SSS. This internal state, typically stored in a Shared Consumer State Store (CSS) using a Shared Database technique, serves two key purposes:

1. **Consistency with the SSS (SSOT):** By keeping track of the last consumed event ID, Projectors ensure they are always in sync with the SSS (Single Source of Truth) up to that point.
2. **Managing Concurrent Access:** The CSS implements mechanisms to manage concurrent access to the Projector's internal state, preventing conflicts when multiple components might attempt to update it simultaneously.

**Query-Oriented Nature and External Data Access**

Projectors reside within the Query Model of a RECQ architecture. This means they cannot directly modify the system state. However, they can access data from other components by making Query-type requests. It's important to remember that these queries might not always reflect the latest state due to the eventual consistency nature of the system.

**Projectors in Action: A Streamlined Approach to Read Models**

By processing events and constructing optimized read models, Projectors empower your application to deliver efficient and consistent query performance. Their focus on sequential processing guarantees strong consistency within the read models, ensuring data integrity for querying purposes. While per-context throughput is bounded, Projectors play a vital role in building reliable and scalable read models within RECQ architectures.

| Capability                  |         |
| --------------------------- | ------- |
| Can handle Command Messages | No      |
| Can handle Query Messages   | No      |
| Can handle Events           | Yes     |
| Can send Command Messages   | No      |
| Can Send Query Messages     | Yes     |
| State type                  | Context |
| Profile                     | C--     |
