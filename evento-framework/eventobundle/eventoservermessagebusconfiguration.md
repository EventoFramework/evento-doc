# EventoServerMessageBusConfiguration

This chapter dives into the configuration options available for the `EventoServerMessageBusConfiguration` class within the Evento Framework. This configuration object holds settings crucial for establishing and maintaining a connection with the Evento server cluster, ensuring reliable message delivery.

**Fields:**

* **addresses (List\<ClusterNodeAddress>)**: This list stores the network addresses (server address and port) of the Evento server nodes within the cluster. The `EventoServerMessageBusConfiguration` constructor takes a variable number of `ClusterNodeAddress` objects, allowing you to specify multiple cluster nodes for redundancy.
* **maxRetryAttempts (int)**: This field defines the maximum number of attempts the application will make to resend a message if the initial delivery fails. The default value is calculated dynamically based on the number of cluster nodes provided in the `addresses` list (number of nodes multiplied by 2).
* **retryDelayMillis (int)**: This value specifies the delay (in milliseconds) between retry attempts for sending a message. The default value is 500 milliseconds.
* **maxReconnectAttempts (int)**: This field defines the maximum number of connection attempts the application will make to re-establish a connection with the cluster if it's lost. A value of -1 signifies unlimited retries. By default, this is set to -1.
* **reconnectDelayMillis (long)**: This value specifies the delay (in milliseconds) between attempts to reconnect to the cluster after a connection loss. The default value is 5000 milliseconds.
* **maxDisableAttempts (int)**: This field defines the maximum number of attempts the application will make to gracefully disable the message bus during application shutdown. Disabling the message bus ensures it stops accepting new messages before the application terminates completely. The default value is 5.
* **disableDelayMillis (int)**: This value specifies the delay (in milliseconds) between attempts to disable the message bus during shutdown. The default value is 5000 milliseconds.

**Explanation of methods:**

The class provides setter methods for each field, allowing you to customize the configuration based on your specific needs. These methods follow a naming convention of `set` followed by the field name with a capital letter (e.g., `setMaxRetryAttempts`). Each setter method returns the `EventoServerMessageBusConfiguration` instance itself, facilitating method chaining for a more concise configuration flow.

**Example Usage:**

The provided code snippet demonstrates how to create an `EventoServerMessageBusConfiguration` object with a single cluster node address and adjust some retry and reconnect settings:

```java
EventoServerMessageBusConfiguration config = new EventoServerMessageBusConfiguration(
    new ClusterNodeAddress(eventoServerHost, eventoServerPort)
)
.setDisableDelayMillis(1000)
.setMaxDisableAttempts(3)
.setMaxReconnectAttempts(30)
.setReconnectDelayMillis(5000);
```

**Additional Notes:**

* Specifying multiple cluster nodes in the `addresses` list enhances fault tolerance. If one node becomes unavailable, the application can attempt to deliver messages to other nodes in the cluster.
* Choosing appropriate values for retry attempts and delays depends on factors like message importance, network reliability, and acceptable latency.

By understanding the configuration options within `EventoServerMessageBusConfiguration`, you can fine-tune the message bus behavior to match your application's specific requirements for message delivery and fault tolerance within the Evento Framework.
