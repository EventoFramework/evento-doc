---
description: Behavioral pattern that defines seven types of components.
---

# RECQ Component Pattern

The RECQ architecture establishes a set of fundamental building blocks, known as RECQ components, designed to implement various functionalities within event-driven microservices. These components are defined with clear yet minimal semantics, enabling the construction of diverse applications without excessive complexity. This minimality is based on empirical observations, as most use cases can be effectively addressed with the component types described below.

<figure><img src="../../.gitbook/assets/image (21).png" alt=""><figcaption><p>RECQ Components Big Picture</p></figcaption></figure>

**Understanding RECQ Component Capabilities**

A crucial aspect of RECQ components is their capability table. This table summarizes the specific actions each component type can perform, along with their scalability and consistency properties in accordance with the CAP theorem. Table 1 provides a generic template for this capability table.

**Table 1: Generic Capability Table for RECQ Components**

* Message Handlers - List of message handlers the component can react to.&#x20;
* Invocations - List of invocations the component can make to other components.&#x20;
* State Type - Indicates if the handler requires a component or instance state.&#x20;
* Consistency (CAP) - Properties of the CAP theorem respected by the component:
  * C: Strong consistency
  * c: Weak consistency within managed message functions
  * A: Strong availability
  * a: Weak availability (except for same resource requests)
  * P: Partitioning tolerance (always present)

| Capability                  |                       |
| --------------------------- | --------------------- |
| Can handle Command Messages | Yes/No                |
| Can handle Query Messages   | Yes/No                |
| Can handle Events           | Yes/No                |
| Can send Command Messages   | Yes/No                |
| Can Send Query Messages     | Yes/No                |
| State type                  | Instance/Component/No |
| CAP Properties              | C/c/A/a/P             |

**State Types in RECQ Components**

There are two primary state types associated with RECQ components:

* **Instance State:** This state represents a single instance of a domain object or a specific resource. Multiple handlers within the same component can operate concurrently, as long as they handle requests for different objects or resources.
* **Component State:** This state is unique to the entire component. Only one handler can be active within a component at any given time when processing a request related to this state.

**Understanding CAP Theorem Properties**

The capability table utilizes specific terms derived from the CAP theorem to define the consistency and availability guarantees of each component type. Here's a breakdown of these terms:

* **C (Strong Consistency):** Components with this property ensure consistency across all replicas, regardless of the message handled. This typically applies to components managing critical data that requires strict consistency.
* **c (Weak Consistency):** These components guarantee consistency only within the context of a managed message function. Data consistency across replicas might have a slight delay, but will eventually converge.
* **A (Strong Availability):** Components with strong availability offer a predictable response time regardless of the request.
* **a (Weak Availability):** These components provide predictable response times except for situations where requests target the same resource concurrently.
* **P (Partitioning Tolerance):** Being a fundamental characteristic of distributed systems, partitioning tolerance is always present in RECQ components, ensuring functionality even if network partitions occur.

In the following sections, we'll delve deeper into each specific RECQ component type, exploring their unique capabilities and limitations within the capability table framework. This analysis will provide a comprehensive understanding of how these components enable the development of scalable and robust event-driven microservices in a RECQ architecture.
