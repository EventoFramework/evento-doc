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

Evento Framework utilizes an abstract class to define the structure of Domain Commands. Here's a typical breakdown of a Domain Command class:

```java
package com.evento.common.modeling.messaging.payload;

/**
 * The DomainCommand class is an abstract class that represents a command related to a domain object.
 * It extends the Command class.
 * Subclasses of DomainCommand must implement the getAggregateId() method to provide the ID of the aggregate the command is targeting.
 */
public abstract class DomainCommand extends Command {

	/**
	 * The invalidateAggregateCaches variable is a boolean flag that determines whether the caches associated with a domain command should be invalidated or not.
	 * <p>
	 * By default, the invalidateAggregateCaches flag is set to false, indicating that the caches should not be invalidated.
	 * <p>
	 * To retrieve the value of the invalidateAggregateCaches flag, use the isInvalidateAggregateCaches() method. This method returns a boolean value: true if the caches should be invalidated
	 * , and false otherwise.
	 * <p>
	 * To set the value of the invalidateAggregateCaches flag, use the setInvalidateAggregateCaches(boolean invalidateAggregateCaches) method. Pass in a boolean value that indicates
	 *  whether the caches should be invalidated or not. The method returns the command object itself.
	 * <p>
	 * The invalidateAggregateCaches flag is a property of the DomainCommand class, which is an abstract class representing a command related to a domain object. The class extends the
	 *  Command class and must implement the getAggregateId() method to provide the ID of the aggregate the command is targeting.
	 * <p>
	 * The Command class is an abstract class that represents a command object that can be used in a software system. It extends the PayloadWithContext class, which is an abstract class
	 *  that represents a payload object with context information. The Command class also declares the getLockId() method, which retrieves the lock ID associated with the command.
	 * <p>
	 * The PayloadWithContext class extends the Payload interface and provides methods to get and set the context of the object. The class also declares the getAggregateId() method,
	 *  which retrieves the ID of the aggregate that the payload is targeting. The setContext(String context) method is used to set the context of the object. The context is a string
	 *  value representing the available context options for certain functionalities within a software system. The context can be accessed using the getContext() method.
	 */
	private boolean invalidateAggregateCaches = false;

	/**
	 * Retrieves whether the aggregate snapshot should be invalidated or not.
	 */
	private boolean invalidateAggregateSnapshot = false;


	@Override
	public String getLockId(){
		return getAggregateId();
	}

	/**
	 * Retrieves whether the caches associated with the command should be invalidated or not.
	 *
	 * @return true if the caches should be invalidated, false otherwise
	 */
	public boolean isInvalidateAggregateCaches() {
		return invalidateAggregateCaches;
	}

	/**
	 * Sets whether the caches associated with the command should be invalidated or not.
	 *
	 * @param invalidateAggregateCaches true if the caches should be invalidated, false otherwise
	 * @param <T>                       the type of the command
	 */
	public <T extends DomainCommand> void setInvalidateAggregateCaches(boolean invalidateAggregateCaches) {
		this.invalidateAggregateCaches = invalidateAggregateCaches;
	}

	/**
	 * Retrieves whether the aggregate snapshot associated with the command should be invalidated or not.
	 *
	 * @return true if the aggregate snapshot should be invalidated, false otherwise
	 */
	public boolean isInvalidateAggregateSnapshot() {
		return invalidateAggregateSnapshot;
	}

	/**
	 * Sets whether the aggregate snapshot associated with the command should be invalidated or not.
	 *
	 * @param invalidateAggregateSnapshot true if the aggregate snapshot should be invalidated, false otherwise
	 * @param <T>                         the type of the command
	 */
	public  <T extends DomainCommand> void setInvalidateAggregateSnapshot(boolean invalidateAggregateSnapshot) {
		this.invalidateAggregateSnapshot = invalidateAggregateSnapshot;
	}
}

```

* **`Command` Extension:** This interface inherits functionalities from the base `Command` interface, likely including a method to access the payload object.
* **`getAggregateId()`:** This method is crucial for routing the command to the appropriate aggregate for handling. It retrieves the ID of the target aggregate.
* **`getLockId()` (Optional):** This method might be used for optimistic locking purposes. By default, it might return `getAggregateId()` to use a locking strategy based on the single aggregate.
* [**Cache Invalidation Control**](domain-command.md#cache-invalidation-mechanism)**:** The `invalidateAggregateCaches` and `invalidateAggregateSnapshot` flags provide fine-grained control over cache invalidation behavior.

**Concrete Domain Command Implementations:**

While the provided code snippet defines an abstact, actual usage involves creating concrete implementations extending `DomainCommand`. These implementations represent specific actions you want to perform on your domain objects. Here's an example:

```java
public class UpdateCustomerCommand extends DomainCommand {

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

#### Cache Invalidation Mechanism

The `invalidateAggregateCaches` flag indicates whether the caches associated with the target aggregate should be invalidated. When set to `true`, the system should invalidate any cached data related to the aggregate after the command is processed. This ensures that subsequent queries retrieve the most up-to-date data.

The `invalidateAggregateSnapshot` flag determines whether the aggregate's snapshot should be invalidated. A snapshot is a persistent representation of the aggregate's state at a specific point in time. By invalidating the snapshot, you force the system to rebuild it from the event stream when it's next requested.

#### Best Practices

* **Strategic Use of Flags:** Carefully consider when to set the `invalidateAggregateCaches` and `invalidateAggregateSnapshot` flags. Excessive cache invalidation can impact performance.
* **Cache Implementation:** The specific implementation of cache invalidation will depend on your caching strategy.
* **Snapshot Management:** Implement a mechanism to efficiently create and manage aggregate snapshots.
* **Error Handling:** Consider error handling for situations where cache invalidation fails.

By effectively utilizing the cache invalidation features of `DomainCommand`, you can optimize system performance and ensure data consistency.
