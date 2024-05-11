# Projector @EventHandler

### Chapter: Reacting to Events in Projectors - The `@EventHandler` Annotation

Projectors, the backbone of materializing domain state in CQRS, rely on event handlers to react to domain events and update the corresponding projection data. This chapter delves into the `@EventHandler` annotation used within projectors to define these event handling methods.

#### Understanding `@EventHandler`

The `@EventHandler` annotation marks a method within your projector class as an event handler. This method is responsible for processing a specific type of domain event and performing the necessary updates on the projection state stored in the database.

Here's a breakdown of the annotation's definition:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface EventHandler {
}
```

* **`@Retention(RetentionPolicy.RUNTIME)`:** Ensures the annotation information is retained at runtime, allowing Evento to access it during application execution.
* **`@Target(ElementType.METHOD)`:** Specifies that the annotation can only be applied to method declarations within your projector class.

#### Implementing `@EventHandler` Methods

An `@EventHandler` method adheres to a specific structure for effective event handling:

* **Event as the First Parameter:** The first parameter of the method must be a subtype of the `Event` class representing the specific event being handled (e.g., `DemoCreatedEvent`).
* **Optional Additional Parameters:** Depending on your specific needs, you might include additional parameters like:
  * `QueryGateway`: This allows the implementation of some cross-domain materialization.
  * `EventMessage<?>`: This provides access to details about the received event, including metadata and timestamp.
  * `Metadata`: This represents metadata associated with the event (often already included in the `EventMessage` object).
  * `Instant`: This represents the timestamp of the event.
* **Void Return Type:** `@EventHandler` methods typically do not have a return value. Their primary purpose is to update the projection state based on the received event.

{% hint style="info" %}
While exploring event handlers in projectors (`@EventHandler`), it's essential to understand the limitations regarding `CommandGateway`. Projectors, by design, focus on materializing the domain state based on events, not modifying the system state directly through commands.

Here's why `CommandGateway` is not typically used within `@EventHandler` methods:

* **Read Model Focus:** Projectors primarily deal with updating the read model (projection state) in the database. This read model serves as the source of data for queries.
* **Event-Driven Updates:** `@EventHandler` methods react to domain events, which represent past changes within the system. These events are not intended to trigger further commands that could modify the current state.
* **Data Consistency:** Sending commands from within event handlers could potentially lead to inconsistencies between the event stream and the actual system state.
{% endhint %}

#### Processing Flow within an `@EventHandler` Method

Here's a breakdown of the typical processing flow within an `@EventHandler` method:

1. **Projection State Update:** The core logic of the event handler lies in modifying the projection state in the database based on the information contained in the domain event. This might involve creating new entries, updating existing data, or deleting data from the projection.
2. **Optional Additional Logic:** In some scenarios, your event handler might perform additional tasks like logging or sending notifications after updating the projection state.

**Example: `@EventHandler` in Action**

```java
@Projector(version = 3)
public class DemoProjector {

    private final DemoRepository demoRepository;

    public DemoProjector(DemoRepository demoRepository) {
       this.demoRepository = demoRepository;
    }

    @EventHandler
    void on(DemoCreatedEvent event,
          QueryGateway queryGateway,
          EventMessage<?> eventMessage,
          Metadata metadata,
          Instant instant) {
       Utils.logMethodFlow(this, "on", event, "BEGIN");
       var now = Instant.now();
       demoRepository.save(new Demo(event.getDemoId(), event.getName(),
             event.getValue(), now, now, null));
       Utils.logMethodFlow(this, "on", event, "END");
    }
 }
```

The provided code example showcases an `@EventHandler` method within a `DemoProjector` class:

* The method is annotated with `@EventHandler`.
* It handles the `DemoCreatedEvent` event.
* It utilizes the `demoRepository` to save a new `Demo` object to the database, reflecting the creation of the Demo Aggregate.
* It logs the processing flow for debugging purposes.

#### Key Takeaways

* `@EventHandler` empowers you to define methods within projectors that listen for specific domain events.
* These methods are responsible for updating the projection state in the database to reflect the changes represented by the events.
* Understanding `@EventHandler` is crucial for building effective projectors that maintain consistency between domain events and the materialized projection state.

In the next chapter, we'll explore different strategies for handling complex event processing scenarios within projectors.
