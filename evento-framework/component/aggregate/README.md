---
description: The Power of Aggregates (@Aggregate)
---

# @Aggregate

This chapter dives into the heart of the RECQ architecture within Evento - the Aggregate, represented by the `@Aggregate` annotation. Here, you'll discover how to define and manage the core unit of consistency in your domain model.

#### Understanding Aggregates

Imagine a complex domain entity, perhaps an "Order" in an e-commerce system. This entity likely consists of related sub-entities, such as order items, customer information, and shipping details. In the RECQ architecture, these related entities are grouped together under an Aggregate, forming a single unit of consistency.

The `@Aggregate` annotation in Evento empowers you to define this Aggregate. By marking a class with `@Aggregate`, you're essentially telling Evento that this class represents the central entity within a cluster of associated objects.

Here are some key characteristics of Aggregates:

* **Single Unit of Consistency:** An Aggregate Rootas a single unit of consistency. This means that all changes to the associated entities within the Aggregate must happen atomically. This ensures data integrity within the domain.
* **Encapsulated State:** The Aggregate encapsulates the current state of all its associated entities. This state is typically represented by an Aggregate State object (discussed in a dedicated chapter).
* **Event Sourcing:** Aggregates are the foundation for Event Sourcing, the technique where all changes to the state are captured as a sequence of immutable events. These events provide a complete history of the Aggregate's state transitions.

#### The `@Aggregate` Annotation

The `@Aggregate` annotation is used to mark a class as an Aggregate Root within the Evento Framework. Here's the breakdown of its definition and key aspects:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Component
public @interface Aggregate {
    /**
     * Retrieves the snapshot frequency for an annotated aggregate class.
     *
     * @return The snapshot frequency for the aggregate class. Returns -1 if no snapshot frequency is specified.
     */
    int snapshotFrequency() default -1;
}
```

Usa il codice con cautela.content\_copy

* **`@Retention(RetentionPolicy.RUNTIME)`:** This ensures that the annotation information is retained at runtime, allowing Evento to access it during application execution.
* **`@Target(ElementType.TYPE)`:** This specifies that the annotation can only be applied to class declarations.
* **`@Component`:** This indicates that the annotated class is a component within the Evento framework.
* **`snapshotFrequency (default -1)`:** This optional parameter allows you to define the frequency at which a snapshot of the current Aggregate State is persisted. A value of -1 signifies that no automatic snapshotting is configured.

#### Implementing Aggregates with `@Aggregate`

```java
@Aggregate(snapshotFrequency = 100)
public class DemoAggregate {
    // ... (code omitted for brevity)
}
```

In this example, the `DemoAggregate` class is annotated with `@Aggregate`. This signifies that it represents the Aggregate Root for the domain concept of "Demo". Additionally, the annotation includes a parameter `snapshotFrequency` set to 100.

#### Snapshot Frequency Explained

Event Sourcing provides a complete history of an Aggregate's state changes. However, replaying a large number of events to rebuild the current state can be computationally expensive, especially for long-lived Aggregates.

The `snapshotFrequency` parameter in the `@Aggregate` annotation addresses this challenge. It allows you to define the frequency at which a snapshot of the current Aggregate State is persisted. This snapshot captures the state of the Aggregate at a specific point in time.

Here's how snapshotting works in Evento:

1. **Event Sourcing:** All changes to the Aggregate state are captured as events.
2. **Snapshotting:** After a certain number of events (defined by `snapshotFrequency`), a snapshot of the current state is persisted.
3. **State Reconstruction:** When retrieving the current state of an Aggregate, Evento first checks for the latest snapshot. If a snapshot exists, it serves as the starting point.
4. **Event Replay:** Only events that occurred after the last snapshot are replayed to reconstruct the most recent state.

By leveraging snapshots, you significantly improve the performance of event replay, especially for Aggregates with a long history.

**In the provided example, `snapshotFrequency` is set to 100. This means that after every 100 events are applied to the `DemoAggregate`, a snapshot of its current state will be persisted.**

The next chapters will provide a more granular look into the building blocks of an Aggregate:

* **Aggregate State:** This chapter explores the object responsible for holding the current state of the Aggregate.
* **AggregateCommandHandler:** We'll discover how commands are handled and processed within an Aggregate.
* **Event Sourcing Handler:** This chapter dives into how events are applied to update the Aggregate State.

By mastering these concepts, you'll be equipped to design and implement robust and scalable microservices using the RECQ architecture and Evento Framework's `@Aggregate` annotation.
