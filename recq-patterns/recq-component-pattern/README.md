---
description: Behavioral pattern that defines seven types of components.
---

# RECQ Component Pattern

The RECQ architecture establishes a set of fundamental building blocks, known as RECQ components, designed to implement various functionalities within event-driven microservices. These components are defined with clear yet minimal semantics, enabling the construction of diverse applications without excessive complexity. This minimality is not merely empirical: classifying handlers by their **trigger** (external request, Command, Query, or Event) and their **state scope** (None, Instance, or Context) and ruling out the ill-formed combinations leaves exactly the seven well-formed component types described below — the number of types follows from the model itself, and practice confirms that most use cases are effectively addressed by them.

<figure><img src="../../.gitbook/assets/image (21).png" alt=""><figcaption><p>RECQ Components Big Picture</p></figcaption></figure>

**Understanding RECQ Component Capabilities**

A crucial aspect of RECQ components is their capability table. This table summarizes the specific actions each component type can perform, along with its state scope and its **consistency–responsiveness profile**. Table 1 provides a generic template for this capability table.

**Table 1: Generic Capability Table for RECQ Components**

* Message Handlers - List of message handlers the component can react to.&#x20;
* Invocations - List of invocations the component can make to other components.&#x20;
* State Type - Indicates if the handler requires a context, instance, or no state.&#x20;
* Profile - The component's consistency–responsiveness reading:
  * C: strong consistency
  * c: weak consistency
  * R: strong responsiveness
  * r: weak responsiveness
  * –: no claim on that dimension

| Capability                  |                     |
| --------------------------- | ------------------- |
| Can handle Command Messages | Yes/No              |
| Can handle Query Messages   | Yes/No              |
| Can handle Events           | Yes/No              |
| Can send Command Messages   | Yes/No              |
| Can Send Query Messages     | Yes/No              |
| State type                  | Instance/Context/No |
| Profile                     | C/c + R/r + –       |

**State Types in RECQ Components**

There are three state scopes associated with RECQ components:

* **No State (None):** The component keeps no state between messages. It can be replicated freely and every replica can serve requests concurrently.
* **Instance State:** This state represents a single instance of a domain object or a specific resource (e.g., one aggregate identified by its key). Multiple handlers within the same component can operate concurrently, as long as they handle requests for different objects or resources.
* **Context State:** This state spans a *context* — a named partition of the event stream that acts as both a spatial and a temporal consistency boundary. Within a context, events are processed strictly in order by a single active handler; different contexts are independent and advance in parallel. The context is therefore also the unit of horizontal scaling for consistent consumers: throughput grows by partitioning the stream into more contexts, not by adding concurrent consumers to the same context.

**Understanding the Consistency–Responsiveness Profile**

The capability table uses a two-letter profile to state what each component type guarantees. Deliberately, these are **not** the letters of the CAP theorem: the profile is a per-component design heuristic about consistency and responsiveness, not an instance of Brewer's system-level result.

* **C (Strong Consistency):** The component processes its state changes under a strict ordering guarantee — observers of its state never see updates out of order or lost.
* **c (Weak Consistency):** Consistency is guaranteed only within the scope of the handled message; state across the system converges eventually.
* **R (Strong Responsiveness):** In the Reactive Manifesto sense — the component reacts within an a-priori bounded time, regardless of the request.
* **r (Weak Responsiveness):** The reaction-time bound holds only for non-contending requests; requests targeting the same resource concurrently may wait on each other.
* **– (No claim):** The component makes no guarantee on that dimension.

In the following sections, we'll delve deeper into each specific RECQ component type, exploring their unique capabilities and limitations within the capability table framework. This analysis will provide a comprehensive understanding of how these components enable the development of scalable and robust event-driven microservices in a RECQ architecture.
