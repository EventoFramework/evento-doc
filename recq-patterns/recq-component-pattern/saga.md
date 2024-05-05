---
description: >-
  A Saga component implements the Saga Pattern to manage distributed
  transactions.
---

# Saga

<figure><img src="../../.gitbook/assets/image (29).png" alt=""><figcaption><p>RECQ Big Picture</p></figcaption></figure>

Sagas are specialized components responsible for coordinating and ensuring consistency across distributed transactions that involve multiple Aggregates or Services. Unlike Projectors that focus on materializing read models, Sagas modify the system state itself.

**Saga Event Handler: The Heart of Transaction Orchestration**

Sagas expose a single key method – the `SagaEventHandler`. This method takes centre stage when a relevant Event (related to the Saga's workflow) arrives:

* **Current State and Event as Inputs:** The `SagaEventHandler` receives both the current state of the Saga and the incoming Event as inputs.
* **State Update and Command/Query Execution:** Based on the current state and the received Event, the Saga can:
  * Update its internal state to reflect the progress of the workflow.
  * Send Command-type messages to relevant Aggregates or Services to trigger state changes within those components.
  * Send Query-type messages to retrieve information from Aggregates or Services to support its decision-making process.

<figure><img src="../../.gitbook/assets/image (31).png" alt=""><figcaption><p>Saga Structure</p></figcaption></figure>

**Local State with Shared Persistence: Balancing Consistency and Performance**

Similar to Aggregates, Sagas maintain an internal state that tracks the progress of the ongoing workflow. However, unlike Aggregates whose state resides in the globally accessible System State Store (SSS), Saga state is persisted in a **Saga Shared Consumer State Store**, which follows the Shared Database pattern.

* **Shared Consumer State Store with Local Focus:**
  * This dedicated state store manages Saga instances of a specific type.
  * It provides methods to save and retrieve the state of individual Saga instances.
* **Consistency Similar to Projectors:**
  * The implementation of the Saga Shared Consumer State Store shares similarities with the Projector Consumer State Store in terms of consistency.
  * However, the details of state retrieval and synchronization across instances are optimized for Saga-specific needs.

**Scalability Constraints: Sequential Processing for Guaranteed Consistency**

Sagas, like Projectors, exhibit limitations in raw processing power due to their focus on consistent cross-component workflows. Their `SagaEventHandler` typically processes events in a sequential manner to ensure the correct order of operations within the Saga workflow. This sequential processing can limit scalability for high-volume workloads involving frequent Sagas.

**Relationship with Projectors: Addressing Different Needs**

Both Projectors and Sagas play critical roles in RECQ architectures, but they cater to distinct needs:

* **Projectors:** Focus on materializing optimized read models from event streams for efficient query processing.
* **Sagas:** Orchestrate complex workflows across multiple components while ensuring consistency within those workflows.

**Sagas in Action: Ensuring Consistency in Complex Workflows**

Sagas are invaluable for managing scenarios where a single action might trigger a sequence of interactions across multiple Aggregates or Services. By orchestrating these interactions and ensuring consistent state changes, Sagas guarantee the overall integrity of distributed transactions within your RECQ application. While scalability constraints might exist, Sagas offer a powerful mechanism for handling complex workflows that require strong consistency across multiple components.

| Capability                  |           |
| --------------------------- | --------- |
| Can handle Command Messages | No        |
| Can handle Query Messages   | No        |
| Can handle Events           | Yes       |
| Can send Command Messages   | No        |
| Can Send Query Messages     | Yes       |
| State type                  | Component |
| CAP Properties              | CP        |
