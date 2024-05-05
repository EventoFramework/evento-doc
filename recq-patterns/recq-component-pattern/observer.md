---
description: Component like Saga but does not hold a state and has no order constraints.
---

# Observer

<figure><img src="../../.gitbook/assets/image (45).png" alt=""><figcaption><p>RECQ Observer Big Picture</p></figcaption></figure>

Observers are specialized components designed to react to and potentially trigger actions based on a single event. Unlike Sagas that manage complex workflows, Observers are lightweight and stateless, making them ideal for simple event-driven reactions.

**The `EventHandler` Method: A Single Event, Focused Action**

Similar to Projectors and Sagas, Observers expose an `EventHandler` method. This method takes centre stage when a relevant Event arrives:

* **Event as Input:** The `EventHandler` receives the relevant Event as input.
* **Action Execution:** Based on the received Event, the Observer can:
  * Send Command-type messages to trigger actions within Aggregates or Services.
  * Send Query-type messages to retrieve information from other components.

<figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption><p>Observer Structure</p></figcaption></figure>

**Stateless Design for Unmatched Scalability**

Unlike Sagas, Observers embrace a completely stateless design. They do not maintain any historical data about past events. This stateless nature allows for exceptional scalability – you can effortlessly add more Observer instances to handle increasing event loads without compromising consistency.

**Event Consumption: Flexibility over Order**

Observers differ from Projectors and Sagas in their approach to event consumption. Projectors and Sagas typically require sequential processing to ensure consistency within read models or workflows. In contrast, Observers do not have strict ordering requirements for event consumption. They simply react to individual events as they arrive.

**Special Case of Sagas: A Simpler Approach**

As the definition highlights, Observers can be considered a special case of Sagas. They operate in a similar fashion, triggering actions based on events, but they lack the internal state and multi-step workflow management capabilities of Sagas. This makes Observers more lightweight and suitable for simpler event-driven reactions.

**Comparison with Services: Reacting vs. Acting**

While Observers share some similarities with Services in their ability to send Command and Query messages, there's a key distinction. Services often represent functionalities directly exposed to external actors, initiating actions within the system. On the other hand, Observers primarily react to events that have already occurred within the system, triggering secondary actions in response.

**Observers in Action: Streamlined Event-Driven Responses**

Observers are valuable for scenarios where you need a component to react to specific events and trigger lightweight actions. They are well-suited for tasks like sending notifications, updating caches, or performing simple data transformations triggered by incoming events. Their stateless nature and flexible event consumption make them highly scalable, allowing you to efficiently handle large volumes of events without impacting system performance.

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | No  |
| Can handle Query Messages   | No  |
| Can handle Events           | Yes |
| Can send Command Messages   | No  |
| Can Send Query Messages     | Yes |
| State type                  | No  |
| CAP Properties              | AP  |
