# @EventSourcingHandler

Event sourcing relies on a fundamental concept: events drive state changes within your domain model. In Evento, the `@EventSourcingHandler` annotation plays a crucial role by enabling you to define methods within your Aggregate Root class that react to these domain events and update the corresponding Aggregate State accordingly.

#### Understanding `@EventSourcingHandler`

Methods annotated with `@EventSourcingHandler` serve as event handlers within your Aggregate. Each handler is responsible for processing a specific type of domain event and applying the necessary state changes to the Aggregate State.

Here's a breakdown of the annotation's definition:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Handler
public @interface EventSourcingHandler {
}
```

* **`@Retention(RetentionPolicy.RUNTIME)`:** This ensures that the annotation information is retained at runtime, allowing Evento to access it during application execution.
* **`@Target(ElementType.METHOD)`:** This specifies that the annotation can only be applied to method declarations within your Aggregate Root class.
* **`@Handler`:** This indicates that the annotated method is a handler for domain events.

#### Implementing `@EventSourcingHandler` Methods

An `@EventSourcingHandler` method adheres to a particular structure for effective event handling:

* **Domain Event as the First Parameter:** The first parameter of the method must be a subtype of the `DomainEvent` class representing the specific event being handled (e.g., `DemoCreatedEvent`).
* **Aggregate State as the Second Parameter:** The second parameter of the method should be of the type `AggregateState` for the corresponding Aggregate (e.g., `DemoAggregateState`). This provides access to the current state of the Aggregate.
* **Optional Additional Parameters:** Depending on your specific needs, you might include additional parameters like:
  * `EventMessage<T extends DomainEvent>`: This offers access to details about the received event, including metadata and timestamp.
  * `Metadata`: This represents metadata associated with the event.
  * `Instant`: This represents the timestamp of the event.
* **Return Type:** The `@EventSourcingHandler` method can have two possible return types:
  * **Modified Aggregate State:** The method can return a new `AggregateState` object that reflects the state of the Aggregate after applying the event. This is the most common approach.
  * **Void:** In some scenarios, the event handler might not need to create a new state object. It can directly modify the provided `AggregateState` object (remember that Evento uses object references).

**Example: `@EventSourcingHandler` in Action**

```java
@EventSourcingHandler
DemoAggregateState on(DemoCreatedEvent event,
					  DemoAggregateState state,
					  EventMessage<DemoCreatedEvent> eventMessage,
					  Metadata metadata,
					  Instant instant) {
	Utils.logMethodFlow(this, "on", event, "ES");
	return new DemoAggregateState(event.getValue());
}

@EventSourcingHandler
DemoAggregateState on(DemoUpdatedEvent event, DemoAggregateState state) {
	Utils.logMethodFlow(this, "on", event, "ES");
	state.setValue(event.getValue());
	return state;
}

@EventSourcingHandler
void on(DemoDeletedEvent event, DemoAggregateState state) {
	Utils.logMethodFlow(this, "on", event, "ES");
	state.setDeleted(true);
}
```

The provided code examples showcase three `@EventSourcingHandler` methods:

* **`on` method for `DemoCreatedEvent`:** This method creates a new `DemoAggregateState` object with the value from the `DemoCreatedEvent`.
* **`on` method for `DemoUpdatedEvent`:** This method directly updates the `value` property within the existing `DemoAggregateState` object based on the `DemoUpdatedEvent`.
* **`on` method for `DemoDeletedEvent`:** This method sets the `deleted` flag to `true` within the `DemoAggregateState` object, signifying the end of the Aggregate's lifecycle.

In essence, these methods demonstrate how `@EventSourcingHandler` allows you to define handlers that listen for specific domain events and transform the Aggregate State accordingly. This maintains consistency between the events and the current state of the Aggregate.

**Key Takeaway:**

Event sourcing events act as instructions for modifying the state. They take the previous state and the current event as input, and based on the event definition, they return (or modify) the state accordingly. The `@EventSourcingHandler` annotation empowers you to define these instructions within your Aggregates, ensuring a clear and maintainable way to react to domain events and manage the overall state of your application.
