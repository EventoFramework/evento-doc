---
description: A Look into Thread-Based Autoscaling
---

# ThreadCountAutoscalingProtocol

In the realm of distributed systems, efficiently managing resources is crucial. Autoscaling protocols provide a powerful mechanism for dynamically adjusting the number of active nodes based on workload demands. This chapter explores a specific approach within the Evento framework - `ThreadCountAutoscalingProtocol`.

**Guarding Against Thread Starvation and Overload:**

This protocol focuses on maintaining an optimal thread pool size within a bundle. It acts as a guardian against two potential issues:

* **Thread Starvation (Boredom):** When the number of active threads consistently stays below a minimum threshold (`minThreadCount`) for a prolonged period (`boredTimeout`), it indicates a lack of work for available threads. This scenario is referred to as "boredom" in the code. To address this, the protocol sends a "ClusterNodeIsBoredMessage". This signal might prompt the cluster to reduce the number of active nodes allocated to this bundle, freeing up resources for busier components.
* **Thread Overload (Suffering):** If the number of messages exceeding the thread pool capacity (`maxThreadCount`) persists for a certain timeframe (`maxOverflowCount`), it suggests the node is struggling to keep up with the workload. This scenario is referred to as "suffering" in the code. To address this, the protocol sends a "ClusterNodeIsSufferingMessage". This signal might trigger the cluster to spawn additional nodes or take other measures to alleviate the overload and ensure smooth operation.

**Core Functionality:**

The `ThreadCountAutoscalingProtocol` class keeps track of the following:

* **`threadCount`:** Maintains the current number of active threads.
* **`overflowCount`:** Tracks consecutive occurrences exceeding `maxThreadCount` after an arrival.
* **`underflowCount`:** Tracks consecutive occurrences falling below `minThreadCount` after a departure.
* **`suffering`:** Boolean flag indicating the node's overloaded state.
* **`bored`:** Boolean flag indicating the node's underutilized state.

The `arrival()` and `departure()` methods manage the thread pool and trigger signals based on these counters:

* `arrival()`: Increments `threadCount` and resets counters (`overflowCount`, `underflowCount`) if necessary. If the thread count surpasses `maxThreadCount`, it increments `overflowCount`. If `overflowCount` reaches `maxOverflowCount` and the node is not already suffering (`suffering` is not set), a "suffering" signal is sent.
* `departure()`: Decrements `threadCount` and resets counters (`overflowCount`, `underflowCount`) if necessary. If the thread count falls below `minThreadCount`, it increments `underflowCount`. If `underflowCount` reaches `maxUnderflowCount` and the node is not already bored (`bored` is not set), a "bored" signal is sent.

**Background Monitoring:**

A separate thread periodically checks for prolonged idleness (no recent departures indicated by `lastDepartureAt` not being updated) and the `bored` flag. If these conditions persist, a "bored" signal is sent to indicate underutilization.

**Utilizing ThreadCountAutoscalingProtocol:**

The provided code snippet demonstrates how to configure a bundle with `ThreadCountAutoscalingProtocol`. The `setAutoscalingProtocolBuilder` method is used to specify the protocol type and its configuration parameters during bundle creation.

```java
EventoBundle.Builder.builder()
       .setBasePackage(DemoQueryApplication.class.getPackage())
       .setConsumerStateStoreBuilder(InMemoryConsumerStateStore::new)
       .setInjector(factory::getBean)
       .setBundleId(bundleId)
       .setBundleVersion(bundleVersion)
       .setAutoscalingProtocolBuilder((es) -> new ThreadCountAutoscalingProtocol(
             es,
             maxThreads,
             minThreads,
             maxOverflow,
             maxUnderflow, 60 * 1000))
```

**In Conclusion:**

`ThreadCountAutoscalingProtocol` offers a practical approach to autoscaling within Evento applications. By dynamically adjusting threads based on message flow, this protocol helps maintain optimal resource utilization and application performance. It's important to consider the workload characteristics and potential overhead when choosing this approach.
