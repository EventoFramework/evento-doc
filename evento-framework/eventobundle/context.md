---
description: The Core Abstraction
---

# Context

The `ConsumerStateStore` class within the Evento Framework serves as the foundation for managing consumer state. It provides a central interface for event consumers (projectors, observers, and sagas) to interact with the Evento server and track their processing progress. This chapter delves into the core functionalities and responsibilities of this abstract class.

**Key Responsibilities:**

* **Event Consumption:**
  * Facilitates consuming events for projectors, observers, and sagas.
  * Handles fetching events from the Evento server in batches based on a specified fetch size.
  * Ensures proper sequencing by tracking the last processed event sequence number for each consumer.
* **State Management:**
  * Provides methods for sagas to access and manipulate their state.
  * Inheriting classes (like `InMemoryConsumerStateStore` or `MysqlConsumerStateStore`) implement specific mechanisms for storing and retrieving saga state.
* **Exclusive Zone Management:**
  * Defines methods for entering and leaving an exclusive zone for a consumer.
  * This mechanism helps prevent concurrent access to a consumer's state during processing, ensuring data consistency.

**Abstract Methods:**

* `consumeEventsForProjector(consumerId, projectorName, context, projectorEventConsumer, fetchSize)`: Consumes events for a specific projector.
* `consumeEventsForObserver(consumerId, observerName, context, observerEventConsumer, fetchSize)`: Consumes events for a specific observer.
* `consumeEventsForSaga(consumerId, sagaName, context, sagaEventConsumer, fetchSize)`: Consumes events for a specific saga.
* `getLastEventSequenceNumberSagaOrHead(consumerId)`: Retrieves the last processed event sequence number for a saga or head consumer.
* `removeSagaState(sagaId)`: Removes the state of a saga identified by its ID. (Implementation specific to subclass)
* `leaveExclusiveZone(consumerId)`: Called when a consumer leaves the exclusive zone. (Implementation specific to subclass)
* `enterExclusiveZone(consumerId)`: Called when a consumer enters the exclusive zone. (Implementation specific to subclass)
* `getLastEventSequenceNumber(consumerId)`: Retrieves the last processed event sequence number for a consumer. (Implementation specific to subclass)
* `setLastEventSequenceNumber(consumerId, eventSequenceNumber)`: Sets the last processed event sequence number for a consumer. (Implementation specific to subclass)
* `getSagaState(sagaName, associationProperty, associationValue)`: Retrieves the stored state of a saga. (Implementation specific to subclass)
* `setSagaState(sagaId, sagaName, sagaState)`: Sets the state of a saga identified by its ID and name. (Implementation specific to subclass)

**Additional Methods:**

* `getObjectMapper()`: Returns the `ObjectMapper` instance used for JSON serialization and deserialization.

**Consumer Implementations:**

While `ConsumerStateStore` provides the core functionalities, specific implementations handle state persistence mechanisms. The Evento Framework offers concrete implementations like:

* `InMemoryConsumerStateStore`: Stores state in-memory, suitable for development or testing environments.
* `MysqlConsumerStateStore`: Leverages MySQL for state persistence, offering durability and scalability.
* `PostgresConsumerStateStore`: Utilizes PostgreSQL for state persistence, providing another option for relational database storage.

These implementations extend `ConsumerStateStore` and provide concrete logic for methods like `removeSagaState`, `leaveExclusiveZone`, `enterExclusiveZone`, `getLastEventSequenceNumber`, and `setLatestEventSequenceNumber`.

Understanding `ConsumerStateStore` is crucial for working with event consumers in the Evento Framework. It establishes a consistent abstraction for event consumption, state management, and concurrency control, allowing developers to focus on business logic within projectors, observers, and sagas.
