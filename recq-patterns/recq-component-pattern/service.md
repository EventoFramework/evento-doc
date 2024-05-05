---
description: >-
  Component that also implements the pattern's Command Model CQRS extension.
  Unlike the aggregate, it does not have a state or its state is external to
  thesystem (not the responsibility of the system)
---

# Service

<figure><img src="../../.gitbook/assets/image (41).png" alt=""><figcaption><p>RECQ Service Big Picture</p></figcaption></figure>

Services act as specialized components responsible for handling interactions with external systems. They serve as bridges between your application and external resources like email services, payment gateways, or any other third-party functionality.

**Command-Driven Operations: Focus on External Actions**

Services primarily utilize a `CommandHandler` method. Unlike Aggregate command handlers, a Service's `CommandHandler` takes only the command message as input. This command encapsulates the desired action for the external system.

**Event Emission: Optional, Not Mandatory**

While not every Service interaction necessitates event emission, some Services might return events. These events could signal the success or failure of the external operation and potentially be used for further processing within the RECQ system.

<figure><img src="../../.gitbook/assets/image (43).png" alt=""><figcaption><p>Service Structure</p></figcaption></figure>

**Limited Query Functionality: Maintaining Domain Focus**

Similar to Aggregates, Services refrain from sending Query-type messages. This aligns with the principles of CQRS, ensuring a clear separation of concerns between command handling and data retrieval.

**Examples in Action: External Communication Made Easy**

* **Email Service:** A Service could be responsible for sending email notifications. The `CommandHandler` within the Service would receive a command containing the email content and recipient details. It would then interact with an external email provider to deliver the message.
* **Payment Processing:** Another example is a Service that delegates payment processing to a third-party provider. The Service's `CommandHandler` would receive a payment command, interact with the payment gateway, and potentially emit an event reflecting the processing outcome.

**Scalability Focus: Availability Reigns Supreme**

Services prioritize availability over strong consistency within the internal system (c). Since Service interactions involve external systems, consistency guarantees are primarily the responsibility of those external providers. However, Services themselves strive to be highly available (a) to ensure smooth communication with external resources. This availability might be subject to the specific implementation of ACID properties (Atomicity, Consistency, Isolation, Durability) within the chosen external system.

**Partitioning Tolerance: A Core Strength**

Like other RECQ components, Services exhibit partitioning tolerance (P). This means they can continue functioning even if network partitions occur, preventing complete system outages due to external communication challenges.

**Services in Action: Enabling Seamless External Interactions**

Services bridge the gap between your application and the external world. They allow for scalable and focused interactions with external systems, ensuring availability for core application functionalities. By leveraging Services, your RECQ architecture can seamlessly integrate with various external resources, enhancing its overall capabilities.

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | Yes |
| Can handle Query Messages   | No  |
| Can handle Events           | No  |
| Can send Command Messages   | Yes |
| Can Send Query Messages     | No  |
| State type                  | No  |
| CAP Properties              | caP |
