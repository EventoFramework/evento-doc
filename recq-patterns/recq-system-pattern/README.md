---
description: Building Blocks for Reactive Microservices
---

# RECQ System Pattern

The RECQ System Pattern defines the high-level modules that make up a RECQ-based application. A RECQ system is composed of exactly **three kinds of modules** working together to create a modular, scalable, and event-driven system:

* [**Components**](component.md)**:** These are self-contained units of software that encapsulate specific functionalities of the application. Each component implements a well-defined business logic and interacts with the rest of the system only through messages. The [RECQ Component Pattern](../recq-component-pattern/) refines them into seven types. Informally they can be grouped by role:
  * **Write side (Aggregates and Services):** Handle commands that modify the system state and publish the resulting events.
  * **Read side (Projectors and Projections):** Materialize and serve read models, kept up to date by subscribing to the published events.
  * **Coordination and reaction (Sagas and Observers):** React to events to orchestrate cross-component workflows or trigger side effects.
  * **Boundary (Invokers):** Bridge the outside world into the system by dispatching commands and queries. Invokers carry no domain state — all domain decisions are delegated to the components they address.
* [**Message Gateway:**](message-gateway.md) This module acts as an intermediary for communication between different components within the system. It handles:
  * Routing each command or query to its single recipient component, based strictly on the message type.
  * Correlating asynchronous responses back to their requests.
* [**System State Store**](system-state-store.md)**:** This persistent storage mechanism is responsible for storing all the events that occur within the system. It serves as the central repository for the complete history of state changes — the system's single source of truth. Components can read from it to rebuild state and subscribe to it to react to state changes.

<figure><img src="../../.gitbook/assets/image (38).png" alt=""><figcaption><p>RECQ System Big Picture</p></figcaption></figure>

**Communication and Event-Driven Interactions (**[**RECQ Communication Patten**](../recq-communication-pattern/)**):**

* Components in a RECQ system communicate with each other primarily through asynchronous messaging. They publish events representing state changes and subscribe to relevant events published by other components.
* When a component performs an action that modifies the system state, it publishes an event to the Event Store. This event contains details about the change that occurred.
* Other components that are interested in these state changes can subscribe to relevant events. When a new event is published, these subscribing components receive a notification and can update their internal state accordingly. This event-driven approach promotes loose coupling between components and enables them to react asynchronously to changes in the system.

**Benefits of the RECQ System Pattern:**

* **Modularity and Scalability:** By breaking down the application into independent components, the system becomes more modular and easier to scale. Individual components can be scaled independently based on their specific load requirements.
* **Maintainability:** Clear separation of concerns makes the application easier to understand, maintain, and modify.
* **Resilience:** Asynchronous communication and event-driven architecture make the system more resilient to failures. If one component fails, it doesn't necessarily bring down the entire system. Other components can continue to operate based on the events they have already received.

**Beyond the Basics:**

While the core RECQ System Pattern defines these essential components, additional considerations can be factored into the design:

* **API Gateway:** An API Gateway can be introduced as a single entry point for external clients to interact with the microservices within the RECQ system.
* **Circuit Breaker Pattern:** Implementing circuit breaker patterns can improve fault tolerance by handling failing services gracefully.
* **Security Mechanisms:** Security considerations like authentication and authorization need to be addressed when designing the communication between components.

**Conclusion:**

The RECQ System Pattern provides a solid foundation for building event-driven, scalable, and maintainable microservices architectures. By understanding the core components and their interactions, developers can design robust applications that can handle the demands of modern software systems.

> RECQ system is a set of computational units called components which they communicate with each other by exchanging messages; if a component has a consequence the system state changes, this information is published as an event in the System State Store, and components can listen for changes of the system state to change their internal state without an explicit message from of another component.

<figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption><p>Sample interaction of modules in a RECQ System</p></figcaption></figure>
