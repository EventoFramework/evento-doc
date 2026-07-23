---
description: Asynchronous Event Distribution with Pub/Sub and Consumer State Stores
---

# System State Store to Component

In a RECQ architecture, the System State Store (SSS) utilizes a pub/sub (publish/subscribe) protocol for distributing information about state changes to interested components. This approach decouples the SSS from individual components and enables efficient event delivery.

**The Role of** [**Consumer State Stores**](../../evento-framework/eventobundle/consumerstatestore/) **(CSS):**

* **Persistent Event Consumption Progress:** CSS modules are introduced to maintain the state of event consumption by individual components. This persistence allows for:
  * **Retry Logic:** If a component fails to process an event, the CSS can track the consumed events and enable retries upon recovery.
  * **Orderly Progress:** The CSS ensures that events are processed in the correct order, even in the face of failures or restarts.
  * **Consistency:** By tracking consumption progress, the CSS helps maintain consistency between the state reflected in the component and the actual state stored in the SSS.

**Communication Protocol:**

* **Pub/Sub with the SSS:**
  * The SSS acts as the publisher in the pub/sub model.
  * Whenever a new event is persisted in the SSS (e.g., after a state change), the SSS publishes the event message to a topic.
  * Topics are named channels that categorize events based on their type or purpose.
* **Subscription by Components:**
  * Components interested in receiving specific events subscribe to relevant topics managed by the SSS.
  * Subscription allows components to filter the events they receive, ensuring they only process the data they need.
* **Consumer State Stores:**
  * Components retrieve their specific consumption progress information from their associated CSS.
  * This information allows components to identify the last successfully processed event and avoid duplicate processing.
  * The CSS can also be used to store additional context related to event consumption by the component.

**Enforcing Single-Active Consumption:**

For consistent consumers (Projectors and Sagas), the CSS is also the mechanism that enforces the single-active-instance-per-context rule:

* **Consumer Lock:** An exclusive lock keyed by consumer and context guarantees that only one instance advances a given context at a time. Replicas that fail to acquire the lock stand by as failover; if the active instance dies or loses its session, a replica takes over from the last recorded checkpoint. Different contexts hold independent locks and advance in parallel.
* **Exactly-Once Gate:** A deduplication record of the last processed event per consumer ensures that after a crash-and-recover, redelivered events are not applied twice.
* **Dead Event Queue:** An event whose processing fails permanently is parked in a dead event queue instead of blocking the stream, and can be inspected and replayed later. Transient failures (a downed collaborator, a timeout) do not dead-letter — the checkpoint stays in place and the event is redelivered with backoff.

<figure><img src="../../.gitbook/assets/image (48).png" alt=""><figcaption><p>System STate Store to Component Communication</p></figcaption></figure>

**Benefits of Pub/Sub and Consumer State Stores:**

* **Scalability:** The pub/sub pattern decouples the SSS from individual components, allowing for independent scaling of both components and the SSS.
* **Flexibility:** Components can subscribe to specific topics, receiving only the events relevant to their functionality.
* **Resilience:** Consumer State Stores enable retry logic and ensure orderly event processing even in the face of failures.
