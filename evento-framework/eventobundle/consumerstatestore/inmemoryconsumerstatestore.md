# InMemoryConsumerStateStore

The `InMemoryConsumerStateStore` class within the Evento Framework serves as a concrete implementation of the abstract `ConsumerStateStore` class. It provides a lightweight solution for storing and managing consumer state information entirely in-memory. This chapter explores the inner workings of `InMemoryConsumerStateStore` and its usage within an Evento application.

**In-Memory Storage:**

* Leverages concurrent hash maps (`ConcurrentHashMap`) to store last processed event sequence numbers for consumers (`lastEventSequenceNumberRepository`) and saga state information (`sagaStateRepository`).
* Since data resides only in memory, it is not persisted across application restarts. This makes `InMemoryConsumerStateStore` suitable for development or testing environments where data persistence is not a primary concern.

**Key Methods:**

* **Constructors:**
  * The primary constructor accepts an `EventoServer` instance for communication with the Evento cluster, a `PerformanceService` instance for performance monitoring, an `ObjectMapper` for serialization/deserialization, and an `Executor` for handling observer execution concurrently.
  * A secondary constructor offers a convenient way to use default values for `ObjectMapper` and `Executor`.
* **`removeSagaState(Long sagaId)`**: Removes the state associated with a specific saga identified by its ID.
* **`leaveExclusiveZone(String consumerId)`**: Releases the lock on the consumer, signifying it has exited the exclusive zone.
* **`enterExclusiveZone(String consumerId)`**: Attempts to acquire a lock for the consumer, ensuring exclusive access to its state during processing.
* **`obtain(Object lockKey)`**: Retrieves a lock from the registry based on a key. If the lock doesn't exist, it creates a new `ReentrantLock` and adds it to the registry. This mechanism ensures thread-safety when accessing consumer state.
* **`getLastEventSequenceNumber(String consumerId)`**: Retrieves the last processed event sequence number for a specific consumer.
* **`setLastEventSequenceNumber(String consumerId, Long eventSequenceNumber)`**: Sets the last processed event sequence number for a consumer.
* **`getSagaState(String sagaName, String associationProperty, String associationValue)`**: Retrieves the stored state for a saga identified by its name, association property, and association value.
* **`setSagaState(Long id, String sagaName, SagaState sagaState)`**: Sets the state for a saga identified by its ID and name.

**Usage Example:**

The provided code snippet demonstrates how to configure `InMemoryConsumerStateStore` within an Evento application using the `EventoBundle.Builder`:

```java
EventoBundle.Builder.builder()
    .setBasePackage(DemoSagaApplication.class.getPackage())
    .setConsumerStateStoreBuilder(InMemoryConsumerStateStore::new)
    ...
    .start();
```

In this example, `InMemoryConsumerStateStore` is specified as the consumer state store provider using the `setConsumerStateStoreBuilder` method. This instructs the Evento framework to utilize in-memory storage for consumer state management.

{% hint style="warning" %}
**Important Considerations:**

* Since `InMemoryConsumerStateStore` relies on in-memory storage, all saga state and consumer state information are lost upon application restarts.
* This implementation is well-suited for development or testing environments where data persistence is not critical.
* For production scenarios where data persistence is essential, consider using alternative implementations like `MysqlConsumerStateStore` or `PostgresConsumerStateStore`.
{% endhint %}

By understanding `InMemoryConsumerStateStore`, you can effectively leverage its lightweight approach for managing consumer state during development or testing within the Evento Framework. Remember to choose the appropriate consumer state store implementation based on your application's specific requirements for data persistence.
