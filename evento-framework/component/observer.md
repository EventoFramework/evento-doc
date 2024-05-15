# @Observer

In the previous chapters, we explored `@Saga` and `@SagaEventHandler` for coordinating long-running transactions and managing state within sagas. This chapter introduces `@Observer`, another fundamental annotation for consuming events within the Evento framework.

#### Understanding `@Observer`

The `@Observer` annotation marks a class as an observer within your Evento application. Observers are lightweight event consumers that react to specific domain events published in the system. Unlike sagas, observers do not maintain their own state and primarily focus on immediate reactions to events.

Here's a breakdown of the key characteristics of `@Observer`:

* **Event Consumption:** Observers act as consumers, listening for and reacting to relevant domain events.
* **Stateless Design:** Observers are designed to be stateless. They process events without maintaining their own state, making them simpler to manage compared to sagas.
* **Immediate Reactions:** Observers typically trigger immediate actions or side effects upon receiving an event. They are suitable for scenarios where you need to perform real-time processing or notifications based on events.

#### Similarities with Other Consumers

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Component
public @interface Observer {
    /**
     * Returns the version of the observer.
     *
     * @return the version of the observer
     */
    int version();
}
```

The definition of `@Observer` shares similarities with annotations for other event consumers in Evento, such as `@Saga` and `@Projector`. This reflects their common role of processing events:

* **`@Component`:** Inherited from `@Component`, indicating the class is a component within Evento.
* **`@Retention(RetentionPolicy.RUNTIME)`:** Ensures the annotation information is retained at runtime for Evento to identify observer classes.
* **`@Target(ElementType.TYPE)`:** Specifies that the annotation can only be applied to class declarations.
* **`version` (Attribute):** Defines the version of the observer logic. Similar to `@Saga`, versioning helps manage changes to the observer's behavior over time.

#### Key Differences from `@Saga`

While sharing some similarities in definition, `@Observer` differs from `@Saga` in its design philosophy:

* **State Management:** Sagas maintain state (`SagaState`) to track their progress throughout a long-running transaction. Observers are stateless and don't manage their own state.
* **Event Handling:** Sagas use `@SagaEventHandler` methods to handle events and update their state. Observers utilize `@EventHandler` methods to react to events, but they don't update state and typically focus on immediate actions.

#### The `DemoObserver` Example

```java
@Observer(version = 1)
public class DemoObserver {

    @EventHandler
    public void on(DemoUpdatedEvent event, CommandGateway commandGateway) {
       Utils.logMethodFlow(this, "on", event, "OBSERVED");
    }

    @EventHandler
    public void on(DemoDeletedEvent event, CommandGateway commandGateway) {
       Utils.logMethodFlow(this, "on", event, "OBSERVED");
    }
}
```

The provided code snippet showcases a `DemoObserver` class:

* It's annotated with `@Observer(version = 1)`, indicating it's an observer with version 1.
* It defines two `@EventHandler` methods:
  * `on(DemoUpdatedEvent)`: This method reacts to `DemoUpdatedEvent`.
  * `on(DemoDeletedEvent)`: This method reacts to `DemoDeletedEvent`.
* Both methods log the event using `Utils.logMethodFlow` and might perform additional processing or side effects based on the event data.

#### Key Takeaways

* `@Observer` provides a way to define lightweight event consumers within Evento.
* Observers are stateless and focus on immediate reactions to relevant domain events.
* Understanding `@Observer` is crucial for implementing scenarios where real-time processing or notifications based on events are necessary.

When to choose `@Observer` vs. `@Saga` depends on your specific needs. If you require complex state management and coordination across multiple events, sagas are the better option. If your use case involves simpler reactions or side effects upon receiving events, observers provide a lightweight and efficient approach.
