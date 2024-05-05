---
description: >-
  Component that can only "invoke" others, it doesn't have an internal state and
  cannot receive messages from within the system.
---

# Invoker

<figure><img src="../../.gitbook/assets/image (39).png" alt=""><figcaption><p>RECQ Invoker Big Picture</p></figcaption></figure>

Invokers serve as the entry points for interacting with your RECQ application. They act as bridges, allowing external entities like user interfaces (UIs), APIs, scheduled tasks, or any other source to trigger actions within the system.

**Manifestations of External Interaction:**

* **REST Controllers:** Invokers can manifest as REST controllers, exposing system functionalities through well-defined RESTful APIs. These controllers receive incoming HTTP requests and translate them into appropriate commands for the internal system.
* **UI Controllers:** Graphical user interfaces (GUIs) can also leverage Invokers. UI controllers capture user interactions and translate them into commands that Invokers can handle.
* **CLI Applications:** Command-line interfaces (CLIs) can be another way to interact with the system. CLI applications send commands directly to Invokers, which then trigger the necessary actions within the RECQ components.
* **Cron Triggers:** Scheduled tasks triggered by cron jobs can also utilize Invokers. These tasks might send commands to initiate specific system processes at predefined intervals.

<figure><img src="../../.gitbook/assets/image (44).png" alt=""><figcaption><p>Invoker Structure</p></figcaption></figure>

**Stateless Design for Unmatched Scalability**

Invokers embrace a stateless design. This means they do not maintain any persistent state information about the interactions they handle. This stateless nature allows for significant scalability – you can effortlessly add more Invoker instances to handle increasing workloads without compromising consistency.

**Availability Reigns Supreme: Always Ready to Serve**

Due to their stateless design and focus on external communication initiation, Invokers prioritize availability (A) within the system. Their primary goal is to be readily accessible for external actors to trigger system actions.

**Partitioning Tolerance: Ensuring Robustness**

Like other RECQ components, Invokers exhibit partitioning tolerance (P). This means they can continue functioning even if network partitions occur. This ensures that external actors can still interact with the system to some extent, even if communication with other internal components might be temporarily disrupted.

**Relationship with Services: A Shared Focus**

While Invokers and Services share some similarities in facilitating external interactions, there's a subtle distinction. Services primarily focus on communication with well-defined external systems like payment gateways or email providers. Invokers, on the other hand, act as a more generic entry point, handling a wider range of external triggers and translating them into commands for the internal system.

**Invokers in Action: Simplifying System Interaction**

By providing a centralized point for external interaction, Invokers simplify system access for various actors. Their stateless design and partitioning tolerance ensure scalability and robustness, allowing your RECQ application to effectively handle incoming requests and commands from diverse external sources. You can leverage different Invoker implementations like REST controllers, GUI controllers, or CLI applications based on your specific use case, offering a flexible approach to user interaction.

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | No  |
| Can handle Query Messages   | No  |
| Can handle Events           | No  |
| Can send Command Messages   | Yes |
| Can Send Query Messages     | Yes |
| State type                  | No  |
| CAP Properties              | AP  |
