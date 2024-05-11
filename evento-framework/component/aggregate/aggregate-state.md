---
description: The Heart of the Aggregate
---

# Aggregate State

The previous chapter explored the concept of Aggregates in Evento, emphasizing their role as the central unit of consistency within your domain model. This chapter delves deeper into the core component that embodies the current state of an Aggregate - the Aggregate State.

#### Understanding Aggregate State

Imagine a complex domain entity like an "Order" in an e-commerce system. The Aggregate Root for "Order" encapsulates various sub-entities like order items, customer information, and shipping details. However, how do we represent the current state of this entire cluster of entities?

This is where the Aggregate State comes into play. In Evento, the Aggregate State is a serializable object responsible for holding the essential properties that define the current state of the Aggregate. It serves as a snapshot of the data associated with the Aggregate Root at any given point in time.

```java
import java.io.Serializable;

/**
 * The AggregateState class represents the state of an aggregate.
 * It provides the functionality to mark the state as deleted.
 */
public abstract class AggregateState implements Serializable {
    private boolean deleted = false;

    /**
     * Determines whether the aggregate state is marked as deleted.
     *
     * @return {@code true} if the aggregate state is marked as deleted, {@code false} otherwise.
     */
    public boolean isDeleted() {
       return deleted;
    }

    /**
     * Sets the deleted flag of the aggregate state.
     *
     * @param deleted {@code true} to mark the aggregate state as deleted, {@code false} otherwise.
     */
    public void setDeleted(boolean deleted) {
       this.deleted = deleted;
    }
}
```

#### Key Responsibilities of Aggregate State

* **State Representation:** The Aggregate State holds the properties that collectively represent the current state of the Aggregate. These properties typically correspond to the domain attributes of the associated entities within the Aggregate.
* **Event Sourcing Integration:** The Aggregate State is intricately linked with Event Sourcing. As events are applied to the Aggregate (discussed in the Event Sourcing Handler chapter), the corresponding properties within the Aggregate State are updated to reflect the state changes.
* **Command Validation:** When a new command is submitted for an Aggregate, the system often needs to verify its consistency with the current state. The Aggregate State plays a crucial role in this validation process. By checking the state properties, the system can determine if the command is applicable to the current state of the Aggregate.
* **Deleted Flag:** The provided `AggregateState` class offers a basic feature - a boolean flag named `deleted`. This flag indicates the end-of-life status of the Aggregate.

#### Code Example: DemoAggregateState

The provided example showcases the `DemoAggregateState` class, a concrete implementation of `AggregateState`:

```java
import lombok.Getter;
import lombok.Setter;
import com.evento.common.modeling.state.AggregateState;

@Setter
@Getter
public class DemoAggregateState extends AggregateState {
    private long value;

    public DemoAggregateState(long value) {
        this.value = value;
    }

    public DemoAggregateState() {
    }
}
```

This example demonstrates a simple Aggregate State with a single property: `value`. As events are applied to the `DemoAggregate`, the `value` property within the `DemoAggregateState` will be updated accordingly.

### Marking an Aggregate for Deletion

When a domain event signifies the completion of an Aggregate's lifecycle, the `deleted` flag within the corresponding `AggregateState` is set to `true`. This action essentially marks the Aggregate for deletion.

The process of deleting an Aggregate in an event store typically follows a two-step approach:

1. **Marking Events as Deleted:** Upon setting the `deleted` flag, the system initiates the process by marking all events associated with the Aggregate as "logically deleted" within the event store
2. **Physical Deletion (Future Optimization):** The actual physical removal of the logically deleted events from the event store doesn't happen immediately. Instead, it's scheduled for a future time based on specific policies:
   * **Time-based:** Events might be physically deleted after a certain period of inactivity (e.g., after a year of being marked as deleted).
   * **Storage Threshold:** When the event store storage reaches a predefined utilization limit, a cleanup process might be triggered to remove old, logically deleted events.

This approach of eventual deletion helps to:

* **Maintain Consistency:** Marking events as deleted first ensures that the system maintains consistency during the deletion process.
* **Optimize Storage:** By physically deleting events only after a specific timeframe or based on storage constraints, the system optimizes storage space in the event store.

#### Impact of the `deleted` Flag

Here's how the `deleted` flag significantly impacts the system's behavior:

* **Command Rejection:** Once an Aggregate is marked as deleted, any new command submitted for that particular Aggregate will be rejected. The system checks the `deleted` flag within the `AggregateState` to verify if the Aggregate is still active. Since it's marked as deleted, the command cannot be applied, reflecting the non-existent state of the Aggregate.

**In summary, the `deleted` flag serves as a trigger for eventual deletion in the event store. It doesn't cause immediate removal but initiates a process that ensures data consistency while optimizing storage space.**

#### Summary

The Aggregate State acts as the foundation for managing the current state of an Aggregate in Evento. It provides a representation of the data, facilitates command validation, and integrates with Event Sourcing. By mastering this concept, you'll be well-equipped to design and implement robust and consistent microservices using the RECQ architecture and Evento's Aggregate framework.

The next chapters will explore the remaining building blocks of an Aggregate:

* **AggregateCommandHandler:** This chapter delves into how commands are handled and processed within an Aggregate.
* **Event Sourcing Handler:** We'll discover how events are applied to update the Aggregate State.
