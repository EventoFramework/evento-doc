---
description: The Heart of Event-Driven State Management
---

# System State Store

The System State Store (SSS) is a crucial component in a RECQ architecture. It serves as the central repository for all events that occur within the system, acting as the Single Source of Truth (SSOT) for the system state. Unlike traditional data stores that hold the current state directly, the SSS maintains an ordered sequence of change-of-state events, providing a complete audit trail of the system's history.

**Key Responsibilities of the SSS:**

* **Publishing Domain Events:**
  * The SSS is responsible for persisting domain events published by components within the system. These events represent atomic changes in the system's state.
  * When a component performs an action that modifies the system state, it publishes an event to the SSS.
  * The event can be associated with an aggregate, which is a group of related domain objects treated as a single unit.
* **Event Stream Retrieval:**
  * Components can retrieve event streams from the SSS.
  * An event stream is an ordered sequence of events starting from a specific point in time.
  * The retrieval can be filtered by:
    * Starting point: Specify the point in time or event sequence number from which to start retrieving events.
    * Aggregate: Retrieve events associated with a specific aggregate or group of related domain objects.
    * Event Type: Filter events based on their specific type (e.g., UserCreatedEvent, OrderPlacedEvent).

<figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption><p>System State Store Structure</p></figcaption></figure>

**Benefits of the SSS:**

* **Single Source of Truth:** The SSS ensures data consistency by maintaining a single definitive source for all events that have occurred within the system.
* **Audit Trail:** The complete sequence of events provides a comprehensive history of the system's state changes, allowing for easier debugging, tracing, and compliance purposes.
* **Replayability:** The system state can be reconstructed at any point in time by replaying the sequence of events stored in the SSS. This enables functionalities like disaster recovery or rolling back to a previous state.

**Additional Considerations:**

* **Event Schema:** The SSS needs a well-defined schema for storing and retrieving events. This schema should capture relevant information about the event, such as timestamp, type, associated aggregate, and event payload.
* **Event Persistence:** The choice of a persistence mechanism for the SSS is crucial. Common options include databases (relational or NoSQL) or dedicated event streaming platforms. The chosen technology should offer scalability, durability, and efficient retrieval capabilities.
* **Event Sourcing vs. Snapshotting:**
  * While the core concept is event storage, some systems utilize snapshots in conjunction with event streams. Snapshots are periodic summaries of the system state at specific points in time. This can improve performance for retrieving the current state compared to replaying the entire event stream.

**Conclusion:**

The SSS plays a vital role in RECQ systems by providing a reliable and consistent mechanism for managing the system state. By understanding its functionalities and considerations, developers can design robust event-driven applications that leverage a complete history of state changes for various purposes.
