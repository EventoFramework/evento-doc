# Service Command

This chapter explores Service Commands, a fundamental concept in Evento Framework for interacting with services within your event-driven architecture. Services are reusable components that encapsulate specific business logic or functionality, often implemented as separate processes or microservices.

#### Understanding Service Commands

Service commands represent a distinct type of command specifically designed to trigger actions or workflows within services. Unlike Domain Commands that target aggregates, Service Commands interact with dedicated service components.

Here's what characterizes a Service Command:

* **Target:** Service commands are directed towards services, which might be separate processes or microservices.
* **Purpose:** They initiate workflows or processes within the service to achieve a specific outcome. These workflows might involve interacting with various resources or databases managed by the service.
* **Functionality:** Similar to domain commands, service commands typically carry data within their payload that specifies the desired action and any necessary information for the service to execute the operation.

#### Benefits of Using Service Commands

Utilizing service commands offers several advantages:

* **Separation of Concerns:** It promotes a clear separation between domain logic (handled by aggregates) and service logic (handled by dedicated services). This improves modularity and reusability.
* **Scalability:** Services can be scaled independently based on their workload, while aggregates focus on domain-specific logic.
* **Flexibility:** Service commands allow for triggering diverse workflows within services, catering to various business logic needs.
* **Structured Communication:** Commands enforce a consistent structure for interacting with services, improving maintainability and understanding of message flows.

#### Implementing a Service Command

Similar to Domain Commands, Evento Framework utilizes abstract classes to define the structure of Service Commands. Here's a breakdown of a typical Service Command class:

```java
package com.evento.common.modeling.messaging.payload;


/**
 * The ServiceCommand abstract class represents a command that can be sent to a service.
 * It extends the Command interface and defines an additional method to retrieve the lock ID associated with the command.
 */
public abstract class ServiceCommand extends Command {

	@SuppressWarnings("SameReturnValue")
	@Override
    public String getLockId(){
		return null;
	}

	@Override
	public String getAggregateId() {
		return getLockId();
	}
}

```

* **`Command` Extension:** This abstract class inherits functionalities from the base `Command` class, likely including a method to access the payload object.
* **Optional `getLockId()`:** This method might be used for locking purposes specific to the service. By default, it might return `null` indicating that locking isn't mandatory for service commands.
* **Override of `getAggregateId()`:** This method overrides the behavior inherited from `Command`. It retrieves the aggregate ID by calling `getLockId()`. This suggests a potential approach where the aggregate ID might be derived from the lock ID if one exists, but it's not the primary target for routing service commands.

**Concrete Service Command Implementations:**

As with Domain Commands, you'll create concrete implementations extending the `ServiceCommand` class for specific service interactions. Here's an example:

```java
public class SendWelcomeEmailCommand extends ServiceCommand {

    private final String customerId;

    // Getters and potentially other service-specific logic
}
```

This `SendWelcomeEmailCommand` extends `ServiceCommand` and specifies the customer ID within its payload. The `getLockId()` method might be implemented to generate a lock ID specific to the service's needs (optional in this example).
