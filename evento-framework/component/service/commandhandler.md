# @CommandHandler

### Chapter: Handling Commands with `@CommandHandler` within Services

Within Evento applications built on the RECQ architecture, services play a crucial role in interacting with the outside world. This chapter explores the `@CommandHandler` annotation, a vital tool for defining methods within services that handle incoming commands.

#### Understanding `@CommandHandler`

The `@CommandHandler` annotation marks a method within your `@Service` class as a command handler. This method is responsible for processing a specific command object, potentially validating its contents, and performing the necessary actions based on the command's intent.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Handler
public @interface CommandHandler {
}
```

Here's a breakdown of the annotation's definition:

* **`@Retention(RetentionPolicy.RUNTIME)`:** Ensures the annotation information is retained at runtime, allowing Evento's `CommandGateway` to discover and execute these methods when commands arrive.
* **`@Target(ElementType.METHOD)`:** Specifies that the annotation can only be applied to method declarations within your service class.
* **`@Handler` (Optional):** In some frameworks like Evento, `@CommandHandler` might inherit from a base annotation like `@Handler` for consistency in marking different handler types.

#### Structure of a `@CommandHandler` Method

A well-structured `@CommandHandler` method typically adheres to the following pattern:

1. **Command Object as First Parameter:** The first parameter of the method must be a subtype of the `Command` class representing the specific type of command being handled (e.g., `NotificationSendCommand`).
2. **Optional Additional Parameters:** Depending on your specific needs, you might include additional parameters like:
   * `CommandGateway` (Optional): This allows sending subsequent commands from within the current command handler (advanced usage).
   * `CommandMessage` (Optional): Provides access to details about the received command message, including metadata and timestamp.
   * `Metadata` (Optional): Represents metadata associated with the command (often already included in the `CommandMessage` object).
   * `Instant` (Optional): Represents the timestamp of the command message.
3. **Command Validation (Optional):** You might include logic to validate the received command's structure and data integrity before proceeding.
4. **Action Execution:** The core logic of the command handler involves performing the necessary actions based on the command. This might involve:
   * Interacting with external APIs (e.g., sending a notification through an email service).
   * Updating internal state (for stateful services).
5. **Event Emission (Optional):** In some scenarios, the command handler might emit domain events after performing its operation to update the system state.

**Example: `@CommandHandler` in Action**

```java
@CommandHandler
NotificationSentEvent handle(NotificationSendCommand command,
							 CommandGateway commandGateway,
							 CommandMessage<NotificationSendCommand> commandMessage) {
	if(command.getBody() == null){
		throw new RuntimeException("error.body.null");
	}
	Utils.logMethodFlow(this, "handle", command, "BEGIN");
	String notificationId = service.send(command.getBody());
	Utils.logMethodFlow(this, "handle", command, "END");
	return new NotificationSentEvent(notificationId, command.getBody());
}

@CommandHandler
void handle(NotificationSendSilentCommand command) {
	Utils.logMethodFlow(this, "handle", command, "BEGIN");
	service.send(command.getBody());
	Utils.logMethodFlow(this, "handle", command, "END");
}
```

The provided code example showcases a `NotificationService` class:

* Both methods are annotated with `@CommandHandler`, indicating they handle commands.
* The first method handles `NotificationSendCommand`, validates the message body, sends the notification through an external service, and emits a `NotificationSentEvent`.
* The second method handles `NotificationSendSilentCommand` and simply sends the notification without emitting an event (potentially a stateless operation).

#### Key Takeaways

* `@CommandHandler` empowers you to define methods within services that act as handlers for specific commands.
* These methods validate, process, and potentially trigger actions based on the incoming commands.
* Understanding `@CommandHandler` is essential for building services that effectively handle commands and interact with the external world within your Evento applications.

Remember, the additional parameters like `CommandGateway`, `CommandMessage`, `Metadata`, and `Instant` provide flexibility for more advanced scenarios, which might be covered in separate chapters.
