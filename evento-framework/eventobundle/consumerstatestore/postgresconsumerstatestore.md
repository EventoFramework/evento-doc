# PostgresConsumerStateStore

The `PostgresConsumerStateStore` class within the Evento Framework extends `ConsumerStateStore` and provides a robust solution for storing and managing consumer state information in a PostgreSQL database. This chapter explores the functionalities and usage of `PostgresConsumerStateStore` for persistent state handling within Evento applications.

**Persistent Storage:**

* Leverages PostgreSQL, a relational database management system, to store consumer state data.
* This enables data persistence across application restarts, ensuring that saga state and consumer progress are preserved.
* Ideal for production environments where data loss prevention is critical.

**Key Methods:**

* **Constructors:**
  * The primary constructor accepts an `EventoServer` instance, a `PerformanceService` instance, a `Connection` object for connecting to the PostgreSQL database, an `ObjectMapper` for serialization/deserialization, and an `Executor` for handling observer execution concurrently.
* **`init()`**: This method is crucial and should be called once before using the consumer state store. It executes Data Definition Language (DDL) statements to create the necessary tables (`evento__consumer_state` and `evento__saga_state`) within the PostgreSQL database if they don't already exist.
* **`removeSagaState(Long sagaId)`**: Deletes the state associated with a specific saga identified by its ID.
* **`leaveExclusiveZone(String consumerId)`**: Releases the advisory lock on the consumer, signifying it has exited the exclusive zone.
* **`enterExclusiveZone(String consumerId)`**: Attempts to acquire an advisory lock for the consumer using PostgreSQL's `pg_advisory_lock` function. This ensures exclusive access to the consumer's state during processing.
* **`getLastEventSequenceNumber(String consumerId)`**: Retrieves the last processed event sequence number for a consumer from the `evento__consumer_state` table.
* **`setLastEventSequenceNumber(String consumerId, Long eventSequenceNumber)`**: Updates the last processed event sequence number for a consumer in the `evento__consumer_state` table.
* **`getSagaState(String sagaName, String associationProperty, String associationValue)`**: Retrieves the stored state for a saga identified by its name, association property, and association value. It utilizes a JSON path query within the PostgreSQL database to efficiently locate the relevant saga state.
* **`setSagaState(Long id, String sagaName, SagaState sagaState)`**: Sets the state for a saga. If an ID is provided (indicating an existing saga), it updates the state for that specific saga. Otherwise, it inserts a new entry for the saga into the `evento__saga_state` table.

**Usage Example:**

The provided code snippet demonstrates how to configure `PostgresConsumerStateStore` within an Evento application using a lambda expression within the `setConsumerStateStoreBuilder` method:

```java
EventoBundle.Builder.builder()
    .setBasePackage(DemoSagaApplication.class.getPackage())
    .setConsumerStateStoreBuilder(((eventoServer, performanceService) -> {
        return new PostgresConsumerStateStore(
                eventoServer,
                performanceService,
                connection); // Connection Object
    }))
    ...
    .start();
```

In this example, a `Connection` object (representing the connection to the PostgreSQL database) is provided during the consumer state store creation. This approach offers flexibility in managing database connections.

**Important Considerations:**

* `PostgresConsumerStateStore` relies on a PostgreSQL database for storage. Ensure you have a properly configured PostgreSQL instance accessible to your Evento application.
* Remember to call the `init()` method to create the necessary tables before using the consumer state store.
* PostgreSQL offers strong consistency guarantees for data persistence.

By utilizing `PostgresConsumerStateStore`, you can ensure that your Evento application maintains a persistent record of consumer state and saga data across restarts. This is essential for production environments where data integrity and reliability are paramount.
