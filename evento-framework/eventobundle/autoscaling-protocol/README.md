---
description: Orchestrating Scalability
---

# Autoscaling Protocol

In the realm of distributed systems, where applications are spread across multiple nodes, ensuring optimal resource utilization is crucial. Autoscaling protocols emerge as a powerful mechanism for dynamically adjusting the number of active nodes based on workload demands. This article explores the core concepts of autoscaling protocols within the Evento framework.

**Abstract Foundation: The `AutoscalingProtocol` Class:**

```java
/**
 * The AutoscalingProtocol class is an abstract class that provides a template for autoscaling protocols in a cluster system.
 */
public abstract class AutoscalingProtocol {
    private final EventoServer eventoServer;

    /**
     * The AutoscalingProtocol class is an abstract class that provides a template for autoscaling protocols in a cluster system.
     */
    protected AutoscalingProtocol(EventoServer eventoServer) {
       this.eventoServer = eventoServer;
    }

    /**
     * This method is called to handle the arrival of a request or message.
     * The behavior of this method should be implemented in the subclass.
     */
    public abstract void arrival();

    /**
     * This method is called to handle the departure of a request or message.
     * The behavior of this method should be implemented in the subclass.
     */
    public abstract void departure();

    /**
     * Sends a bored signal to the cluster.
     * Throws an exception if the message sending fails.
     *
     * @throws Exception if the message sending fails
     */
    protected void sendBoredSignal() throws Exception {
       eventoServer.send(new ClusterNodeIsBoredMessage(eventoServer.getBundleId(), eventoServer.getInstanceId()));
    }

    /**
     * Sends a suffering signal to the cluster indicating that the node is suffering.
     * Throws an exception if the message sending fails.
     *
     * @throws Exception if the message sending fails
     */
    protected void sendSufferingSignal() throws Exception {
       eventoServer.send(new ClusterNodeIsSufferingMessage(eventoServer.getBundleId()));
    }
}
```

The provided code snippet showcases the `AutoscalingProtocol` class, which serves as an abstract foundation for defining autoscaling behaviors within Evento applications. It outlines the core functionalities:

* **Template for Subclasses:** This abstract class provides a blueprint for concrete implementations tailored to specific scaling strategies.
* **EventoServer Dependency:** The constructor injects an `EventoServer` instance, granting access to cluster information and message sending capabilities.

**Arrival and Departure Signals:**

* **`arrival()`:** This abstract method signifies the arrival of a new request or message. Subclasses are responsible for implementing the logic to assess this arrival and potentially trigger scaling actions based on their chosen strategy.
* **`departure()`:** This abstract method signifies the completion of handling a request or message. Similar to `arrival()`, subclasses can leverage this method to evaluate the workload and initiate scaling decisions if necessary.

**Signaling Boredom and Suffering:**

* **`sendBoredSignal()`:** This method enables a node to indicate its underutilization to the cluster by sending a `ClusterNodeIsBoredMessage`. The message contains the bundle and instance ID for identification.
* **`sendSufferingSignal()`:** This method allows a node to signal overload to the cluster by sending a `ClusterNodeIsBoredMessage`. This message includes only the bundle ID, indicating that the entire bundle (potentially composed of multiple components) is experiencing high load.

**Collaboration with Tracing Agents:**

The article mentions that autoscaling protocols work in conjunction with tracing agents. Tracing agents provide valuable insights into message flow and component workload, which can be leveraged by autoscaling protocols to make informed decisions.

**Scaling Decisions Based on Bundle Context:**

The article emphasizes that autoscaling protocols operate at the bundle level. When composing components within a bundle, it's essential to consider their combined resource consumption to make effective scaling decisions.

**A Glimpse into the Next Chapter:**

The next chapter promises to explore a concrete example - a thread count autoscaling protocol. This implementation will likely demonstrate how to assess thread pool utilization within the `arrival()` and `departure()` methods to trigger scaling actions based on workload.

**In Conclusion:**

Autoscaling protocols empower Evento applications to adapt to changing workloads. By understanding the core principles of the `AutoscalingProtocol` class and its interaction with tracing agents, developers can design custom scaling strategies that optimize resource utilization and application performance within distributed systems. The upcoming example of a thread count autoscaling protocol will provide a practical illustration of these concepts.
