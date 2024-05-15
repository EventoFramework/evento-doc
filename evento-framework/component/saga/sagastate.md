# SagaState

In the previous chapter, we explored the concept of sagas in Evento, highlighting their role in coordinating long-running transactions. This chapter dives into `SagaState`, a fundamental building block for managing the state of a saga throughout its lifecycle.

#### Understanding `SagaState`

The `SagaState` class serves as an abstract superclass for defining the state associated with a saga instance. It provides core functionalities for managing the saga's lifecycle and data.

```java
/**
 * An abstract class representing the state of a saga.
 */
public abstract class SagaState implements Serializable {
    private boolean ended = false;
    private final HashMap<String, String> associations = new HashMap<>();

    /**
     * Determines if the saga is ended.
     * @return true if the saga is ended, false otherwise
     */
    public boolean isEnded() {
       return ended;
    }

    /**
     * Sets the ended flag of the saga state.
     *
     * @param ended the value indicating if the saga is ended
     */
    public void setEnded(boolean ended) {
       this.ended = ended;
    }

    /**
     * Sets an association between an event field name and a value.
     *
     * @param eventFieldName the name of the event field
     * @param value          the value to associate with the event field
     */
    public void setAssociation(String eventFieldName, String value) {
       associations.put(eventFieldName, value);
    }
    /**
     * Retrieves the value associated with the specified event field name.
     *
     * @param eventFieldName the name of the event field
     * @return the value associated with the event field, or null if no association exists
     */
    public String getAssociation(String eventFieldName) {
       return associations.get(eventFieldName);
    }

    /**
     * Removes the association between an event field name and its value.
     *
     * @param eventFieldName the name of the event field to remove the association from
     */
    public void unsetAssociation(String eventFieldName) {
       associations.remove(eventFieldName);
    }
}
```

Here's a breakdown of the key features of `SagaState`:

* **State Management:** Sagas are stateful, meaning they track relevant information during the workflow execution. `SagaState` provides a foundation for storing and manipulating this data.
* **Ended Flag:** The `ended` property indicates whether the saga has completed its execution. When a saga is set as `ended` (often triggered by an event signifying completion or cancellation), it's typically **removed from the system**. This ensures efficient resource management and prevents unnecessary processing of finished sagas.
* **Associations:** The `associations` map allows storing key-value pairs to associate data extracted from events with meaningful names. These associations become crucial for referencing specific event data within the saga logic.

#### Essential Methods of `SagaState`

* **`isEnded()` and `setEnded(boolean ended)`:** These methods allow checking and setting the `ended` flag, which determines if the saga has finished processing its events. Setting the flag to `true` often initiates the saga's removal from the system.
* **`setAssociation(String eventFieldName, String value)`, `getAssociation(String eventFieldName)`, and `unsetAssociation(String eventFieldName)`:** These methods manage the `associations` map. You can set key-value pairs to associate extracted data from event properties with meaningful names for easier retrieval later in the saga logic.

#### The `DemoSagaState` Example

```java
@Setter
@Getter
public class DemoSagaState extends SagaState {
    private long lastValue;

}
```

The provided code snippet showcases a `DemoSagaState` class:

* It extends `SagaState`, inheriting its core functionalities.
* It defines a `longValue` property specific to the `DemoSaga` workflow.
* It might be extended further to include additional state properties relevant to the saga's logic.

#### Using Associations in `@SagaEventHandler` (Next Chapter)

The `associations` map plays a vital role when working with `@SagaEventHandler` methods (covered in the next chapter). These methods handle events and often leverage associations to retrieve data previously stored from event properties using `setAssociation`. This establishes a connection between events and the saga's state, enabling informed decision-making within the saga logic.

#### Key Takeaways

* `SagaState` provides the foundation for managing the state of a saga instance in Evento.
* It offers functionalities to track the saga's lifecycle (ended flag) and store key-value associations for data extracted from events.
* Understanding `SagaState` is essential for building effective sagas that can manage complex workflows and maintain their state across events.

The next chapter will explore `@SagaEventHandler`, focusing on how sagas react to events and utilize `SagaState` for informed decision-making within the workflow.
