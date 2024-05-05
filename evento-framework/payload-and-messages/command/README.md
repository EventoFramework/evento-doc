# Command

**Understanding CommandMessage and Command Interface is crucial for sending instructions and triggering actions within your event-driven applications built with Evento Framework.** These concepts allow you to define commands with target aggregates, potentially leverage locking mechanisms, and structure them within messages for effective communication.

**Command Interface:**

```java
package com.evento.common.modeling.messaging.payload;


/**
 * The Command interface represents a command object that can be used in a software system.
 * It extends the Payload interface, which represents a payload object that can be used in a software system.
 */
public interface Command extends Payload {
    /**
     * Retrieves the ID of the aggregate that the command is targeting.
     *
     * @return The aggregate ID as a string.
     */
    String getAggregateId();

    /**
     * Retrieves the lock ID associated with the ServiceCommand.
     *
     * @return The lock ID associated with the ServiceCommand.
     */
    @SuppressWarnings("SameReturnValue")
    String getLockId();

}
```

* **Purpose:** This interface defines the core functionalities expected of a command object.
* **Inheritance:** It typically extends the `Payload` interface, ensuring commands adhere to basic payload functionalities (carrying data).
* **Methods:**
  * `getAggregateId()`: Retrieves the ID of the aggregate that the command targets. This is crucial for routing the command to the appropriate aggregate for handling.
  * `getLockId()` (with potential `@SuppressWarnings` annotation): Might retrieve a lock ID associated with the command for data consistency during execution (implementation details might vary).

#### Aggregate ID

The `aggregateId` plays a crucial role in managing event streams and ensuring data consistency within your Event-Driven system. It acts as a unique identifier for an aggregate instance. This ID is used for two key purposes:

1. **Retrieving Event Stream:** By providing the `aggregateId` to the system's State Store, you can efficiently retrieve the complete sequence of events (event stream) that belongs to that specific aggregate. This allows you to reconstruct the current state of the aggregate by replaying all the events in the stream.
2. **Storing Generated Events:** When a Domain Command is processed by an aggregate, it triggers the creation of new events that reflect the state change. These newly generated events are then stored within the system's State Store, but crucially, they are associated with the same `aggregateId` as the command that triggered them. This ensures that all events related to a particular aggregate instance are grouped together in the event stream, maintaining a clear audit trail and simplifying retrieval for later processing or rebuilding the aggregate's state.

In simpler terms, the `aggregateId` acts like a reference point that connects commands, generated events, and the overall state of an aggregate, ensuring data consistency and organized event storage within your Event-Driven system.

**CommandMessage:**

```java
package com.evento.common.modeling.messaging.message.application;

import com.evento.common.modeling.messaging.payload.Command;

/**
 * The CommandMessage class represents a message that carries a command payload.
 * It extends the Message class and is meant to be subclassed for specific types of commands.
 * <p>
 * CommandMessage objects can be used to send commands and invoke command handler methods.
 * They contain the command payload, metadata, timestamp, and other related information.
 * @param <T> the Command payload for this message
 */
public abstract class CommandMessage<T extends Command> extends Message<T> {

    private String aggregateId;
    private String lockId;

    /**
     * CommandMessage is a subclass of Message that represents a message carrying a command payload.
     * It is meant to be subclassed for specific types of commands.
     *
     * @param command The command payload of this message
     */
    public CommandMessage(T command) {
       super(command);
       this.aggregateId = command.getAggregateId();
       this.lockId = command.getLockId();
    }

    /**
     * The CommandMessage class represents a message that carries a command payload.
     * It extends the Message class and is meant to be subclassed for specific types of commands.
     * <p>
     * CommandMessage objects can be used to send commands and invoke command handler methods.
     * They contain the command payload, metadata, timestamp, and other related information.
     */
    public CommandMessage() {
    }

    /**
     * Returns the name of the command.
     *
     * @return The name of the command.
     */
    public String getCommandName() {
       return super.getPayloadName();
    }

    /**
     * Retrieves the ID of the aggregate the command is targeting.
     *
     * @return The ID of the aggregate.
     */
    public String getAggregateId() {
       return aggregateId;
    }

    /**
     * Sets the ID of the aggregate that the command is targeting.
     *
     * @param aggregateId The ID of the aggregate as a string.
     */
    public void setAggregateId(String aggregateId) {
       this.aggregateId = aggregateId;
    }


    /**
     * Sets the lock ID for the ServiceCommandMessage.
     *
     * @param lockId The lock ID to be set.
     */
    public void setLockId(String lockId) {
       this.lockId = lockId;
    }

    /**
     * Retrieves the lock ID associated with the ServiceCommandMessage.
     *
     * @return The lock ID associated with the ServiceCommandMessage.
     */
    public String getLockId() {
       return lockId;
    }


    @Override
    public void setPayload(T payload) {
       super.setPayload(payload);
       this.lockId = payload.getLockId();
       this.aggregateId = payload.getAggregateId();
    }
}
```

* **Abstract Concept:** There might not be a concrete `CommandMessage` class in Evento Framework.
* **Functionality:** The concept likely refers to the usage of the `Message` abstract class (discussed earlier) to create messages specifically for commands.
* **Implementation:** When sending a command, a developer would likely:
  1. Create a concrete command object implementing the `Command` interface (e.g., `UpdateCustomerCommand`).
  2. Use this command object as the payload when constructing a `Message` object using the `Message` class constructor (`new Message(commandObject)`).

**Understanding the Relationship:**

* The `Command` interface defines the expected structure and behavior of a command object.
* The `Message` class provides a way to encapsulate the command object (as the payload) along with other message details (type, timestamp, etc.) within a message structure.

**Benefits of this approach:**

* **Separation of Concerns:** The `Command` interface focuses on the command itself, while the `Message` class handles the overall message structure.
* **Flexibility:** Different command types can be implemented while adhering to the core functionalities defined in the `Command` interface.
* **Structured Communication:** The `Message` class ensures commands are sent with additional context (type, timestamp) for better processing within the event-driven system.

**Additional Considerations:**

* Evento Framework might have specific ways to handle serialization and deserialization of commands within `SerializedPayload` objects (not shown in the provided code snippets).
* There might be helper classes or annotations to simplify command creation and message construction.
