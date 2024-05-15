# @SagaEventHandler

In the previous chapter, we explored `SagaState`, the foundation for managing a saga's state. This chapter dives into `@SagaEventHandler`, a crucial annotation for defining methods that react to events within a saga instance.

#### Understanding `@SagaEventHandler`

The `@SagaEventHandler` annotation marks methods inside a saga class that handle specific events. These methods become event listeners, responding to relevant domain events published within the system.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Handler
public @interface SagaEventHandler {
    /**
     * Initializes the annotated method.
     *
     * @return true if the method is an initialization handler, false otherwise.
     */
    boolean init() default false;

    /**
     * Retrieves the name of the property used to associate events with a Saga instance.
     *
     * @return The name of the association property as a {@code String}.
     */
    String associationProperty();
}
```

Here's a breakdown of the key aspects of `@SagaEventHandler`:

* **Event Listeners:** Methods annotated with `@SagaEventHandler` act as event listeners for the saga instance. They are invoked whenever a matching event is published.
* **State Management:** Sagas leverage `@SagaEventHandler` methods to process events, update their state (`SagaState`), and potentially trigger actions based on the event data and current saga state.
* **`init` (Optional):** This boolean flag indicates whether the method is an initialization handler. When set to `true` (default is `false`), the method is called when the saga is first created in response to a starting event.
* **`associationProperty` (Mandatory):** This attribute specifies the name of the property within the handled event that should be used to associate the event with a saga instance. The saga framework uses this property to link incoming events with the appropriate saga instances.

#### Requirements for `@SagaEventHandler` Methods

There are two mandatory requirements for methods annotated with `@SagaEventHandler`:

1. **First Argument as Event:** The first argument of the method must be the type of the event it handles. This allows the method to access the event data for processing.
2. **`associationProperty` Setting:** You must define the `associationProperty` attribute within the annotation. This property name should correspond to a field within the handled event that uniquely identifies the saga instance the event relates to.

#### Utilizing `SagaState` and Optional Parameters

* **`SagaState`:** `@SagaEventHandler` methods can leverage the `SagaState` object (often the return type) to manage the saga's state throughout its lifecycle. They might update the state based on the event data and the current saga state.
* **Optional Parameters:** `@SagaEventHandler` methods can also receive additional optional parameters:
  * `CommandGateway` and `QueryGateway`: These gateways allow interacting with the domain by sending commands or executing queries within the saga logic.
  * `EventMessage<?>`: Provides access to the entire event message object.
  * `Instant`: Offers the timestamp of the event occurrence.
  * `Metadata`: Grants access to any metadata associated with the event.

#### Example: `DemoSaga` Event Handlers

```java
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
```

The provided `DemoSaga` class showcases several `@SagaEventHandler` methods:

* **`on(DemoCreatedEvent)`:** This method is marked with `init=true`, indicating it's the initialization handler for the saga. It creates a new `DemoSagaState`, sets the association based on the `demoId` from the event, and returns the state object.
* **`on(DemoUpdatedEvent)`:** This method handles `DemoUpdatedEvent`. It checks a condition based on the event's value and potentially interacts with the domain using gateways. It updates the `lastValue` property in the `SagaState` and returns the updated state.
* **`on(DemoDeletedEvent)`:** This method handles `DemoDeletedEvent`. It retrieves data using the `QueryGateway`, sends a notification using the `CommandGateway`, and marks the `SagaState` as ended.

**Note:** This example doesn't showcase the optimal usage of sagas for handling eventual consistency concerns.

#### Key Takeaways

* `@SagaEventHandler` empowers sagas to react to relevant events and manage their state accordingly.
* Understanding `@SagaEventHandler` is essential for building robust sagas that coordinate long-running workflows within Evento.
* Effective use of `SagaState` and optional parameters allows for informed decision-making and potential interactions with the domain within the saga logic.

The next chapter might explore a different saga usage example that highlights eventual consistency concerns and how sagas can handle them.
