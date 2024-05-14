# @Service

The Evento Framework adopts the principles of the RECQ architecture, and within this context, the `@Service` annotation plays a crucial role. This chapter delves into how `@Service` is used to define services that interact with the outside world and potentially manage the internal state.

#### Understanding `@Service`

The `@Service` annotation marks a class within your Evento application as a service. Services are responsible for performing specific tasks or operations that fall outside the domain logic itself. They often interact with external systems or persist data for future use.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Component
public @interface Service {
}
```

Here's a breakdown of the annotation's definition:

* **`@Retention(RetentionPolicy.RUNTIME)`:** Ensures the annotation information is retained at runtime, allowing Evento to identify services within your application.
* **`@Target(ElementType.TYPE)`:** Specifies that the annotation can only be applied to class declarations.
* **`@Component`:** Inherits from the `@Component` annotation, indicating that the annotated class is a component within the Evento framework.

#### Services in RECQ Architecture

The RECQ architecture emphasizes the separation of concerns between domain logic and external interactions. Services act as a bridge between the internal domain events and the outside world, performing the necessary actions based on commands or interacting with external systems.

There are two main types of services within RECQ:

* **Stateless Services:** These services perform actions without maintaining any internal state. A common example is sending notifications through an external API (like sending an email notification upon an event).
* **Stateful Services:** These services manage and persist their own state. For instance, a payment gateway service might store information about ongoing transactions.

#### Using `@Service` with Command Handlers

Services leverage `@CommandHandler` methods to handle incoming commands. These command handlers typically follow this pattern:

1. **Command Reception:** The command handler receives a specific command object as input.
2. **Command Validation (Optional):** You might include validation logic within the handler to ensure the received command is valid before proceeding.
3. **Interaction with External Systems:** The service interacts with external systems (e.g., databases, APIs) based on the command requirements.
4. **Event Emission (Optional):** In some scenarios, the service might emit domain events after performing its operation to update the system state.

**Example: `@Service` in Action**

```java
@Service
public class NotificationService {

    private final ExternalNotificationService service;

    public NotificationService(ExternalNotificationService service) {
       this.service = service;
    }

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
}
```

The provided code example showcases a `NotificationService` class:

* The class is annotated with `@Service`, indicating it's a service component.
* It has a constructor that injects an `ExternalNotificationService` dependency.
* It defines two `@CommandHandler` methods:
  * The first method handles `NotificationSendCommand` and validates the presence of a message body before sending the notification through the external service and emitting a `NotificationSentEvent`.
  * The second method handles `NotificationSendSilentCommand` and simply sends the notification without emitting an event (potentially a stateless operation).

#### Key Takeaways

* `@Service` helps define classes that perform specific operations outside the domain logic.
* Services can be stateless, interacting with external systems without managing internal state, or stateful, maintaining their own data.
* `@Service` often works in conjunction with `@CommandHandler` methods to handle commands and trigger interactions with external systems.

By understanding `@Service`, you can effectively build services that bridge the gap between your domain and the external world in your Evento applications.
