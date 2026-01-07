---
description: Orchestrating Long-Running Transactions
---

# @Saga

The RECQ architecture emphasizes handling complex workflows that might span multiple services and data sources. In this context, the `@Saga` annotation plays a vital role in defining classes that coordinate these long-running transactions.

#### Understanding `@Saga`

The `@Saga` annotation marks a class within your Evento application as a saga. Sagas are stateful components responsible for managing the flow of a complex business process that involves multiple events. They ensure data consistency across these events and potentially interact with various services or projections.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Component
public @interface Saga {
    /**
     * Returns the version of the method.
     *
     * @return the version of the method
     */
    int version();
}
```

Here's a breakdown of the annotation's definition:

* **`@Retention(RetentionPolicy.RUNTIME)`:** Ensures the annotation information is retained at runtime, allowing Evento to identify saga classes.
* **`@Target(ElementType.TYPE)`:** Specifies that the annotation can only be applied to class declarations.
* **`@Component`:** Inherits from the `@Component` annotation, indicating that the annotated class is a component within the Evento framework.
* **`version` (Attribute):** Defines the version of the saga logic. Versioning helps manage changes to the saga's behavior over time.

#### Sagas in the RECQ Pattern

The RECQ pattern promotes modularity and separation of concerns. Sagas bridge the gap between domain events and actions that require coordination across services. They provide a way to manage complex workflows that cannot be easily handled by individual services.

Here are some key characteristics of sagas:

* **Long-Running Transactions:** Sagas manage workflows that might span multiple events over time.
* **State Management:** They maintain their own state to track the progress of the workflow.
* **Event-Driven:** Sagas react to domain events emitted within the system.
* **Coordinating Actions:** They might interact with various services, projections, or send commands to trigger actions based on the workflow logic.

#### The `DemoSaga` Example

```java
@Saga(version = 1)
public class DemoSaga {

    @SagaEventHandler(init = true, associationProperty = "demoId")
    public DemoSagaState on(DemoCreatedEvent event,
                      CommandGateway commandGateway,
                      QueryGateway queryGateway,
                      EventMessage<?> message) {
       Utils.logMethodFlow(this, "on", event, "BEGIN");
       DemoSagaState demoSagaState = new DemoSagaState();
       demoSagaState.setAssociation("demoId", event.getDemoId());
       demoSagaState.setLastValue(event.getValue());
       Utils.logMethodFlow(this, "on", event, "END");
       return demoSagaState;
    }

    @SagaEventHandler(associationProperty = "demoId")
    public DemoSagaState on(DemoUpdatedEvent event,
                      DemoSagaState demoSagaState,
                      CommandGateway commandGateway,
                      QueryGateway queryGateway,
                      EventMessage<?> message) throws ExecutionException, InterruptedException {
       Utils.logMethodFlow(this, "on", event, "BEGIN");
       if (event.getValue() == 12)
       {
          var demo = queryGateway.query(new DemoRichViewFindByIdQuery(event.getDemoId())).get();
          System.out.println(jump(commandGateway, demo.getData().toString()));
       }
       demoSagaState.setLastValue(event.getValue());
       Utils.logMethodFlow(this, "on", event, "END");
       return demoSagaState;
    }

    @SagaEventHandler(associationProperty = "demoId")
    public DemoSagaState on(DemoDeletedEvent event,
                      DemoSagaState demoSagaState,
                      CommandGateway commandGateway,
                      QueryGateway queryGateway,
                      EventMessage<?> message) throws ExecutionException, InterruptedException {
       Utils.logMethodFlow(this, "on", event, "BEGIN");
       System.out.println(this.getClass() + " - on(DemoDeletedEvent)");
       var demo = queryGateway.query(new DemoRichViewFindByIdQuery(event.getDemoId())).get();
       var resp = commandGateway.send(new NotificationSendSilentCommand("lol" + demo.getData().toString())).get();
       System.out.println(resp);
       demoSagaState.setEnded(true);
       Utils.logMethodFlow(this, "on", event, "END");
       return demoSagaState;
    }

    public NotificationSentEvent jump(CommandGateway commandGateway, String msg) {
       return sendNotification(commandGateway, msg);
    }

    public NotificationSentEvent sendNotification(CommandGateway commandGateway, String msg) {
       return commandGateway.send(new NotificationSendCommand(msg)).get();
    }


}
```

The provided code snippet showcases a `DemoSaga` class:

* It's annotated with `@Saga(version = 1)`, indicating it's a saga with version 1.
* It defines state management logic (covered in the next chapter) and several `@SagaEventHandler` methods:
  * The `on` method for `DemoCreatedEvent` initializes the saga state.
  * The `on` method for `DemoUpdatedEvent` updates the saga state and performs conditional logic based on the updated value.
  * The `on` method for `DemoDeletedEvent` performs actions upon deletion, including sending a notification and marking the saga as ended.
* These methods demonstrate how sagas react to domain events and manage the workflow accordingly.

#### Key Takeaways

* `@Saga` helps define classes that coordinate long-running transactions within your Evento application.
* Sagas manage state, react to domain events, and potentially interact with services or projections to fulfill complex business processes.
* Understanding `@Saga` is crucial for building robust workflows that span multiple events and actions within the RECQ architecture.

The next chapter will delve deeper into `Saga State` management, an essential aspect of working with sagas in Evento.
