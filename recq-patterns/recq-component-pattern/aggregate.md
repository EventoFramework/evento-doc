---
description: >-
  An aggregate is a component that implements the Command Model of the CQRS
  pattern. Is defined as such because it is the implementation of a Domain
  Driven Design Aggregate.
---

# Aggregate

<figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption><p>RECQ Aggregate Big Picture</p></figcaption></figure>

An Aggregate represents a single, well-defined entity within your domain model. It encapsulates the state and logic associated with that entity, acting as the central hub for managing its lifecycle.

**State Reconstruction and Replay:**

The state of an Aggregate is not directly stored within the component itself. Instead, it's reconstructed by replaying a sequence of events pertaining to that specific Aggregate stored in the System State Store (SSS). This event stream provides a complete and auditable history of all state changes the Aggregate has undergone.

**The Command Handler: Orchestrator of Change**

Aggregates boast a single "handle" method – the command handler. This handler plays a pivotal role in processing commands that modify the state of the Aggregate. It takes two key inputs:

1. **Command Message:** This message encapsulates the specific action to be performed on the Aggregate.
2. **Aggregate State:** Represented as a sequence of events retrieved from the SSS, this provides the current state of the Aggregate necessary for the command handler to make informed decisions.

<figure><img src="../../.gitbook/assets/image (23).png" alt=""><figcaption><p>Aggregate Structure</p></figcaption></figure>

**Transformation Through Commands:**

The command handler acts as the brain of the Aggregate. It analyzes the incoming command message in the context of the current state (event history). Based on this analysis, it performs two possible actions:

* **Generate a State Change Event:** If the command is valid, the handler generates a new event that reflects the state change resulting from the command execution.
* **Return an Error:** If the command violates any business rules or constraints, the handler returns an error message indicating the failure.

Note that this is a structural rule, not a convention: a command handler emits **exactly one event** (or fails). When a business action seems to require multiple events, the RECQ resolutions are to model a single *richer* event that carries the whole outcome, or to delegate the follow-up steps to a Saga that reacts to the first event.

**Publishing the Change Story:**

If a state change event is generated, it's published to the SSS. This event serves as a record of the change and allows for eventual consistency to be achieved across the system.

**Domain Logic at Its Core:**

Aggregates are the primary architects of the domain logic within a RECQ architecture. They encapsulate the business rules and constraints that govern the behavior of your domain entities.

**Restrictions on Queries and Consistency:**

Command handlers within Aggregates are restricted from sending Query-type messages. This stems from the principle of CQRS and ensures that all information required for command processing is present within the Aggregate's state (event history). Additionally, since queries offer eventual consistency, relying on them for command validation could lead to inconsistencies.

**Command Dependency and Communication:**

While Aggregates cannot send queries, they can execute other commands. This allows for complex domain logic that might involve interactions with other Aggregates. For instance, generating a unique identifier across the system might involve sending a command to a dedicated "Unique ID Generation" Aggregate.

**Scalability and Consistency Considerations:**

Maintaining strong consistency for Aggregate state requires serializing the commands that target the same aggregate instance. This weakens responsiveness (r): a command may wait behind another command addressed to the same instance, so the reaction-time bound holds only for non-contending requests. The guarantee is localized to the instance — commands for different aggregate instances proceed in parallel, and the aggregate's profile is therefore **Cr**: strongly consistent per instance, weakly responsive under contention.

In essence, RECQ Aggregates are powerful building blocks that provide a well-defined and consistent approach to managing domain entities and their associated logic within event-driven microservices architectures.

| Capability                  |                             |
| --------------------------- | --------------------------- |
| Can handle Command Messages | Yes                         |
| Can handle Query Messages   | No                          |
| Can handle Events           | No                          |
| Can send Command Messages   | Yes                         |
| Can Send Query Messages     | No                          |
| State type                  | Instance (by Aggregate Key) |
| Profile                     | Cr                          |
