---
description: The Building Block of Event-Driven Microservices
---

# Component

A RECQ component is a self-contained unit of software that implements a well-defined set of functionalities within a RECQ-based application. It plays a crucial role in promoting modularity, loose coupling, and asynchronous communication within the system.

**Properties of a RECQ Component:**

* [**Isolation**](https://www.reactivemanifesto.org/glossary#Isolation)**:**
  * **Temporal Isolation:** Components operate independently and asynchronously without relying on other components to be available at any specific time.
  * **Spatial Isolation:** Components don't need knowledge about the location or existence of other components in the system. This concept is also known as Location Transparency.
* **Containment:**
  * Components encapsulate the logic and resources they need to fulfill their responsibilities.
  * This aligns with the concept of aggregation in Domain-Driven Design, where tightly coupled entities are grouped together within a component.
* [**Delegation**](https://www.reactivemanifesto.org/glossary#Delegation)**:**
  * Components focus on a well-defined set of tasks and delegate any unrelated functionalities to other components or external services.

**Capabilities of a RECQ Component:**

* **Message Handling:**
  * Components can receive messages addressed specifically to them.
  * They can process the message and optionally respond with a reply message to the sender.
  * This capability allows components to implement reactive behaviour and respond to external actions.
* **Internal State Management:**
  * Components can maintain a persistent internal state that reflects their specific data and information relevant to their functionalities.
* **Event-Driven Communication:**
  * Components can publish System State Change Events whenever their internal state changes due to processing a message.
  * Publishing events allows other components to be notified about these changes and potentially update their own state accordingly.
  * Components can also subscribe to specific System State Change Events published by other components.
  * By consuming events, components can react asynchronously to changes in the system without needing direct communication with the originating component.
* **Messaging Other Components:**
  * Components can send messages to other components within the system.
  * This capability allows for inter-component communication to coordinate activities and share information.
* **Replicability:**
  * A RECQ component can be replicated across multiple instances to achieve horizontal scaling.
  * The design of the component should ensure consistency even with multiple instances operating concurrently.

> Strict definition:
>
> * Can **receive messages** and may **respond** to them
> * Can manage a persistent **internal state**
> * Can **publish** events
> * Can **subscribe** to events
> * Can **send messages**
> * Must be **replicable**

**Benefits of RECQ Components:**

* **Modularity:** Breaking down the application into independent components improves code organization and maintainability.
* **Loose Coupling:** Asynchronous messaging and event-driven communication reduce dependencies between components, making the system more flexible and adaptable.
* **Scalability:** Components can be scaled independently based on their specific load requirements.
* **Resilience:** Event-driven communication and independent components enhance system resilience. If one component fails, others can continue operating based on the events they've received.

**Conclusion:**

RECQ components are the fundamental building blocks of a RECQ architecture. By adhering to the principles of isolation, containment, and delegation, and leveraging their capabilities effectively, developers can create robust, scalable, and maintainable event-driven microservices applications.
