# @AggregateCommandHandler

This chapter dives into the heart of processing commands within an Aggregate in Evento. You'll explore the `@AggregateCommandHandler` annotation and discover how to effectively handle command events to manage state changes in your domain model.

#### The `@AggregateCommandHandler` Annotation

The `@AggregateCommandHandler` annotation serves as the cornerstone for defining methods that handle commands within an Aggregate. It essentially marks a method within your Aggregate Root class as responsible for processing a specific domain command.

Here's a breakdown of the annotation's definition:

Java

```java
/**
 * Annotation used to mark a method as an aggregate command handler.
 *
 * @see com.evento.common.modeling.annotations.component.Aggregate
 * @see <a href="https://docs.eventoframework.com/evento-framework/component/aggregate/aggregatecommandhandler">AggregateCommandHandler</a>
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Handler
public @interface AggregateCommandHandler {
	/**
	 * Checks if the method is marked as an aggregate initializer.
	 *
	 * @return {@code true} if the method is an initializer, otherwise {@code false}.
	 */
	boolean init() default false;
}
```

Usa il codice con cautela.content\_copy

* **`@Retention(RetentionPolicy.RUNTIME)`:** This ensures that the annotation information is retained at runtime, allowing Evento to access it during application execution.
* **`@Target(ElementType.METHOD)`:** This specifies that the annotation can only be applied to method declarations within your Aggregate Root class.
* **`@Handler`:** This indicates that the annotated method is a handler for domain commands.
* **`init (default false)`:** This optional parameter allows you to mark a specific command handler as an initializer for the Aggregate. Initializers are responsible for creating a new Aggregate instance.

#### Implementing `@AggregateCommandHandler` Methods

An `@AggregateCommandHandler` method must adhere to a specific structure to effectively handle commands:

* **Domain Command as the First Parameter:** The first parameter of the method must be a subtype of the `DomainCommand` class representing the specific command being handled.
* **Aggregate State as the Second Parameter:** The second parameter of the method should be of the type `AggregateState` for the corresponding Aggregate. This provides access to the current state of the Aggregate.
* **Optional Additional Parameters:** Depending on your specific requirements, you might include additional parameters like `CommandGateway` for sending follow-up commands or `CommandMessage` for accessing details about the received command.
* **Return Type: Domain Event Object:** The `@AggregateCommandHandler` method must return a subtype of the `DomainEvent` class. This returned event object signifies the outcome of processing the command and encapsulates the state change resulting from the command's execution.

#### Processing Flow within an `@AggregateCommandHandler` Method

Here's a breakdown of the typical processing flow within an `@AggregateCommandHandler` method:

1. **Validation Phase:**
   * The method performs validations on the received `DomainCommand` object. This ensures that the command is syntactically correct (all fields have the provided formats) and semantically consistent (the proposed domain change aligns with the current state of the Aggregate). Techniques like assertions might be used for validation.
2. **Event Forging Phase:**
   * Assuming the command passes validation, the method constructs a new `DomainEvent` object that represents the state change resulting from the command's execution. This event object encapsulates the details of the change that will be applied to the Aggregate State.

**Example: `@AggregateCommandHandler` in Action**

```java
@AggregateCommandHandler(init = true)
DemoCreatedEvent handle(DemoCreateCommand command,
                   DemoAggregateState state,
                   CommandGateway commandGateway,
                   CommandMessage<DemoCreateCommand> commandMessage) {
    Utils.logMethodFlow(this, "handle", command, "BEGIN");
    commandGateway.send(new NotificationSendCommand(command.getName())).get();
    Assert.isTrue(command.getDemoId() != null, "error.command.not.valid.id");
    Assert.isTrue(command.getName() != null, "error.command.not.valid.name");
    Assert.isTrue(command.getValue() >= 0, "error.command.not.valid.value");
    Utils.doWork(1200);
    Utils.logMethodFlow(this, "handle", command, "END");
    return new DemoCreatedEvent(
          command.getDemoId(),
          command.getName(),
          command.getValue());
}

@EventSourcingHandler
DemoAggregateState on(DemoCreatedEvent event,
                  DemoAggregateState state,
                  EventMessage<DemoCreatedEvent> eventMessage) {
    Utils.logMethodFlow(this, "on", event, "ES");
    return new DemoAggregateState(event.getValue());
}

@AggregateCommandHandler
DemoUpdatedEvent handle(DemoUpdateCommand command,
                   DemoAggregateState state) {

    Utils.logMethodFlow(this, "handle", command, "BEGIN");
    Utils.doWork(1100);
       Utils.logMethodFlow(this, "handle", command, "END");
    return new DemoUpdatedEvent(
          command.getDemoId(),
          command.getName(),
          command.getValue());
}

@EventSourcingHandler
DemoAggregateState on(DemoUpdatedEvent event, DemoAggregateState state) {
    Utils.logMethodFlow(this, "on", event, "ES");
    state.setValue(event.getValue());
    return state;
}
```

The provided code examples showcase two `@AggregateCommandHandler` methods:

* **`handle` method for `DemoCreateCommand`:** This method validates the `DemoCreateCommand` and, upon successful validation, creates a `DemoCreatedEvent` reflecting the new Aggregate state.
* **`handle` method for `DemoUpdateCommand`:** This method validates the `DemoUpdateCommand` and, if valid, creates a `DemoUpdatedEvent` representing the updated state.

### ptional Parameters for `@AggregateCommandHandler` Methods

While the core structure of an `@AggregateCommandHandler` method involves the `DomainCommand` and `AggregateState` parameters, there are several optional parameters you can leverage to enhance command handling capabilities:

* **`CommandGateway (Optional)`:** This parameter provides access to the `CommandGateway` interface. This interface allows you to send follow-up commands within the same transactional context as the current command. For instance, after handling a `DemoUpdateCommand`, you might want to send a separate command to notify an external system about the update. By utilizing `CommandGateway`, you can achieve this within the same transaction, ensuring data consistency.

{% hint style="warning" %}
While the `CommandGateway` provides a convenient way to trigger follow-up commands within your `@AggregateCommandHandler` methods, it's crucial to be mindful of potential challenges regarding cross-domain consistency.

**The Issue:**

Event sourcing systems are not inherently transactional across multiple Aggregates. When you send a new command using `CommandGateway` within an `@AggregateCommandHandler` method, there's no guarantee that both commands will succeed or fail atomically.

Here's a scenario to illustrate the concern:

1. You handle a command in an Aggregate and use `CommandGateway` to send a follow-up command to another Aggregate.
2. The first command successfully processes and generates an event.
3. However, the follow-up command sent to the other Aggregate might fail due to validation errors or other unforeseen circumstances.

In this situation, you've potentially modified the state of your first Aggregate but haven't achieved the intended outcome in the second Aggregate. This can lead to inconsistencies in your overall domain model.

emember, the key lies in understanding the potential implications of cross-domain consistency when using `CommandGateway`. By employing alternative strategies like Sagas complex workflows, you can ensure a more robust and consistent domain model in your Evento applications.
{% endhint %}

* **`CommandMessage<T extends DomainCommand> (Optional)`:** This parameter provides access to the `CommandMessage` object that encapsulates the received `DomainCommand`. The `CommandMessage` offers additional information about the command, including:
  * **Metadata:** The `CommandMessage` might contain metadata associated with the command. This metadata could include information like the source of the command (e.g., user ID) or tracing information for debugging purposes.
  * **Timestamp:** The `CommandMessage` typically holds a timestamp representing the time the command was received by the system. This can be useful for auditing purposes or ensuring temporal ordering of events.

**Remember:** While `CommandMessage` provides access to metadata and timestamp, these are often already available within the received `DomainCommand` object itself. The decision to use `CommandMessage` depends on your specific needs and whether you require additional information beyond the core command data.

* **`Instant (Optional)`:** This parameter allows you to explicitly specify the timestamp for the domain command being created. By default, most event creation methods within Evento likely use the current system time. However, in specific scenarios, you might want to set a custom timestamp for the event.
* **`Metadata (Optional)`:** The same Metadata object carried by the message.

By strategically using these optional parameters, you can create more versatile and informative `@AggregateCommandHandler` methods within your Evento Aggregates.

```java

@AggregateCommandHandler(init = true)
DemoCreatedEvent handle(DemoCreateCommand command,
                   DemoAggregateState state,
                   CommandGateway commandGateway,
                   CommandMessage<DemoCreateCommand> commandMessage,
                   Metadata metadata,
                   Instant instant) {
                   // implementation
}
```

**In essence, the `@AggregateCommandHandler` annotation empowers you to define clear and concise methods within your Aggregate Root class that handle domain commands, perform validations, and generate corresponding domain events to manage state changes.**

The next chapter will explore how these generated domain events are applied to update the Aggregate State within Evento.
