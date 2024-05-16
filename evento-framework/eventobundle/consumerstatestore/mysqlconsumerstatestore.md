# MysqlConsumerStateStore

The `MysqlConsumerStateStore` class in the Evento Framework extends `ConsumerStateStore` and provides a solution for storing and managing consumer state information within a MySQL database. This chapter explores the functionalities and usage of `MysqlConsumerStateStore` for persistent state handling in Evento applications.

**MySQL Storage:**

* Leverages MySQL, a popular open-source relational database management system, to store consumer state data.
* Offers a familiar and widely adopted alternative to PostgreSQL for persistent state management.
* Ensures that saga state and consumer progress are preserved across application restarts.

**Key Methods:**

* **Constructors:**
  * Similar to `PostgresConsumerStateStore`, the primary constructor accepts an `EventoServer` instance, a `PerformanceService` instance, a `Connection` object for connecting to the MySQL database, an `ObjectMapper` for serialization/deserialization, and an `Executor` for handling observer execution concurrently.
* **`init()`**: This method is crucial and should be called once before using the consumer state store. It executes Data Definition Language (DDL) statements to create the necessary tables (`evento__consumer_state` and `evento__saga_state`) within the MySQL database if they don't already exist.
* **`removeSagaState(Long sagaId)`**: Deletes the state associated with a specific saga identified by its ID.
* **`leaveExclusiveZone(String consumerId)`**: Releases the lock on the consumer, signifying it has exited the exclusive zone.
* **`enterExclusiveZone(String consumerId)`**: Attempts to acquire a lock for the consumer using MySQL's `GET_LOCK` function. This ensures exclusive access to the consumer's state during processing.
* **`getLastEventSequenceNumber(String consumerId)`**: Retrieves the last processed event sequence number for a consumer from the `evento__consumer_state` table.
* **`setLastEventSequenceNumber(String consumerId, Long eventSequenceNumber)`**: Updates the last processed event sequence number for a consumer in the `evento__consumer_state` table.
* **`getSagaState(String sagaName, String associationProperty, String associationValue)`**: Retrieves the stored state for a saga identified by its name, association property, and association value. It utilizes a JSON path query within the MySQL database to efficiently locate the relevant saga state.
* **`setSagaState(Long id, String sagaName, SagaState sagaState)`**: Sets the state for a saga. If an ID is provided (indicating an existing saga), it updates the state for that specific saga. Otherwise, it inserts a new entry for the saga into the `evento__saga_state` table.

**Usage Example:**

The provided code snippet demonstrates how to configure `MysqlConsumerStateStore` within an Evento application using a lambda expression within the `setConsumerStateStoreBuilder` method:

```java
EventoBundle.Builder.builder()
    .setBasePackage(DemoSagaApplication.class.getPackage())
    .setConsumerStateStoreBuilder(((eventoServer, performanceService) -> {
        return new MysqlConsumerStateStore(
                eventoServer,
                performanceService,
                connection); // Connection Object
    }))
    ...
    .start();
```

In this example, a `Connection` object (representing the connection to the MySQL database) is provided during the consumer state store creation.

**Important Considerations:**

* `MysqlConsumerStateStore` relies on a MySQL database for storage. Ensure you have a properly configured MySQL instance accessible to your Evento application.
* Remember to call the `init()` method to create the necessary tables before using the consumer state store.
* MySQL offers a strong foundation for persistent state management, with a rich ecosystem of tools and libraries.

By choosing `MysqlConsumerStateStore`, you can leverage the familiarity and widespread adoption of MySQL for persistent state management within your Evento applications. This ensures data integrity and reliability across application restarts.
