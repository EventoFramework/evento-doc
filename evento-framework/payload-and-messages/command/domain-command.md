# Domain Command

This chapter dives into the concept of Domain Commands within Evento Framework, a key element for triggering actions and modifications related to your domain objects in an event-driven architecture.

#### Understanding Domain Commands

Domain commands represent a specific type of command used to interact with domain objects in your application. Domain objects, referred to as Aggregates, encapsulate domain logic and data pertaining to a particular entity or concept within your problem domain.

Here's what characterizes a Domain Command:

* **Focus:** Domain commands are designed to be processed by the aggregates themselves.
* **Purpose:** They trigger actions or modifications on the state of the targeted aggregate.
* **Functionality:** Commands typically carry data within their payload that specifies the desired action and any necessary information for the aggregate to perform the change.

#### Benefits of Using Domain Commands

Utilizing domain commands offers several advantages:

* **Separation of Concerns:** It promotes a clean separation between domain logic (handled by aggregates) and infrastructure concerns (like message routing and persistence).
* **Structured Communication:** Domain commands enforce a consistent structure for interacting with aggregates. This includes the target aggregate ID for routing and potential default locking mechanisms.
* **Domain-Centric Design:** Domain commands encourage a focus on domain concepts and behavior, promoting a clear understanding of your domain model.
* **Reusability:** By extending the base `Command` interface, domain commands leverage existing functionalities while adding domain-specific requirements.

#### Implementing a Domain Command

Evento Framework utilizes interfaces to define the structure of Domain Commands. Here's a typical breakdown of a Domain Command interface:

```java
package com.evento.common.modeling.messaging.payload;

/**
 * The DomainCommand class is an abstract class that represents a command related to a domain object.
 * It extends the Command class.
 * Subclasses of DomainCommand must implement the getAggregateId() method to provide the ID of the aggregate the command is targeting.
 */
public interface DomainCommand extends Command {
	String getAggregateId();

	@Override
	default String getLockId(){
		return getAggregateId();
	}
}

```

* **`Command` Extension:** This interface inherits functionalities from the base `Command` interface, likely including a method to access the payload object.
* **`getAggregateId()`:** This method is crucial for routing the command to the appropriate aggregate for handling. It retrieves the ID of the target aggregate.
* **`getLockId()` (Optional):** This method might be used for optimistic locking purposes. By default, it might return `getAggregateId()` to use a locking strategy based on the single aggregate.

**Concrete Domain Command Implementations:**

While the provided code snippet defines an interface, actual usage involves creating concrete implementations extending `DomainCommand`. These implementations represent specific actions you want to perform on your domain objects. Here's an example:

```java
public class UpdateCustomerCommand implements DomainCommand {

    private final String customerId;
    private final String newEmail;

    // Getters, setters, and potentially other domain-specific logic

    @Override
    public String getAggregateId() {
        return customerId;
    }

    // Optional implementation for getLockId() if needed
}
```

This `UpdateCustomerCommand` extends `DomainCommand` and specifies the customer ID and new email address within its payload. The `getAggregateId()` method returns the customer ID, allowing the command to be routed to the appropriate customer aggregate for processing.
