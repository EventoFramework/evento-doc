---
description: This pattern describes the modules that make up a RECQ architecture.
---

# RECQ System Pattern

A RECQ System consists of the following modules:

* [**Components**](component.md) – Self-contained portions of software that implement application logic.
* [**Message Gateway**](message-gateway.md) – Component that manages communication between components in terms of requests and responses.
* [**System State Store**](system-state-store.md) – Component responsible for persisting system state in the form of event logs.

So a RECQ system is a set of computational units called components that communicate with each other by exchanging messages; if a component causes the system state to change, this information is published as an event in the System State Store, furthermore, the components can listen for system state changes to change their internal state without an explicit message from another component.

<figure><img src="../../.gitbook/assets/image (38).png" alt=""><figcaption><p>RECQ System Big Picture</p></figcaption></figure>

So a RECQ system is a set of computational units called components which they communicate with each other by exchanging messages; if a component has a consequence the system state changes, this information is published as an event in the System State Store, and components can listen for changes of the system state to change their internal state without an explicit message from of another component.

<figure><img src="../../.gitbook/assets/image (34).png" alt=""><figcaption><p>Example interactin in a RECQ System</p></figcaption></figure>
