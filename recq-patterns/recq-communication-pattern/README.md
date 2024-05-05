---
description: The Language of Event-Driven Microservices
---

# RECQ Communication Pattern

The RECQ Communication Pattern defines the structure and expected behaviour of messages exchanged between components within a RECQ system. This pattern promotes asynchronous communication and loosely coupled interactions, facilitating the development of scalable and resilient applications.

**Message Types in RECQ:**

* **Commands:** Messages that represent requests to modify the system state. They trigger actions within the system and potentially result in state changes. Commands are typically sent from components (e.g., user interface) to Command Services.
* **Events:** Messages published as a consequence of a successful command execution. They represent a change that has occurred in the system state. Events are published by Command Services and can be consumed by other components interested in those changes.
* **Queries:** Messages used to retrieve data from the system without modifying the state. They are typically sent from components (e.g., user interface) to Query Services.
* **View (Query Responses):** Messages containing the data retrieved by a Query Service in response to a query message. They are sent from Query Services back to the requesting component.
* **Void Responses (Optional):** Simple messages sent back by a component in response to a command, indicating successful processing without additional data. (Consideration: Some systems might prefer specific success/failure messages with details instead of a simple void response.)

<figure><img src="../../.gitbook/assets/image (46).png" alt=""><figcaption><p>RECQ Payloads</p></figcaption></figure>

**Message Handling Protocols:**

* [**Component-to-Component**](component-to-component.md) **Communication:**
  * This pattern utilizes asynchronous message exchange (e.g., using message queues or brokers) for communication between components. This promotes loose coupling as components don't need to wait for a response synchronously.
  * The specific protocol (e.g., request/reply, publish/subscribe) might vary depending on the message type and the desired level of interaction.
* [**Component-to-System State Store**](component-to-system-state-store.md)**:**&#x20;
  * Upon successful command execution, the Command Service publishes an event to the System State Store.
  * The event contains details about the state change caused by the command.
* [**System State Store-to-Component**](system-state-store-to-component.md)**:**
  * The System State Store utilizes a publish/subscribe pattern for event distribution.
  * Components can subscribe to specific events or event types that they are interested in.
  * When a new event is published to the store, subscribed components receive a notification and can react asynchronously to the state change.

**Benefits of the RECQ Communication Pattern:**

* **Asynchronous Communication:** Enables loosely coupled components to interact without waiting for synchronous responses.
* **Event-Driven Architecture:** Promotes reactivity and allows components to react to state changes asynchronously.
* **Scalability:** Asynchronous messaging facilitates the horizontal scaling of components based on their load.
* **Resilience:** Event-driven communication makes the system more resilient to failures. If a component fails, it won't necessarily block other components from functioning.

**Conclusion:**

The RECQ Communication Pattern provides a clear structure for message exchange within a RECQ architecture. By understanding the different message types and their corresponding handling protocols, developers can design event-driven microservices that communicate efficiently and asynchronously, leading to scalable and maintainable applications.
