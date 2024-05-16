---
description: Partitioning Events for Focused Processing
---

# Context

The Evento framework introduces the concept of "Context" to enable focused processing of events within a bundle. This chapter explores how contexts are defined, used, and empower efficient event handling based on specific criteria.

**Understanding Context:**

* Context acts as a property associated with an event, allowing for event categorization.
* You can set context for an event during its creation using the `setContext` method.
* Contexts are typically derived from the event data itself or extracted from the accompanying metadata.

**Setting Event Context:**

The provided code snippet demonstrates how to set context for an event within an AggregateCommandHandler:

```java
return new DemoCreatedEvent(
        command.getDemoId(),
        command.getName(),
        command.getValue())
    .setContext(ContextUtils.getContextFromMetadata(metadata));
```

In this example, the context is retrieved from the `metadata` object and assigned to the newly created `DemoCreatedEvent`.

**Context and Event Partitioning:**

* Contexts serve as a powerful mechanism for partitioning event streams.
* Events sharing the same context are considered part of the same independent partition.
* This enables focused processing, where consumers dedicated to specific contexts handle only relevant events.

**Configuring Contexts in Evento Bundle:**

The `setContexts` method within `EventoBundle.Builder` allows you to define contexts for your bundle:

<pre class="language-java"><code class="lang-java">EventoBundle.Builder.builder()
...
<strong>.setContexts(Map.of(DemoProjector.class.getSimpleName(), Set.of("UK", "IT")))
</strong><strong>...
</strong></code></pre>

Here, a map is used to associate a consumer class (e.g., `DemoProjector`) with a set of contexts (e.g., "UK" and "IT").

**Event Consumption with Context Awareness:**

* When an Evento bundle starts, it instantiates a consumer for each context defined within the bundle configuration.
* These consumers are responsible for processing events that share their designated context.
* Evento filters events based on context during consumption, ensuring that each consumer receives only relevant events.

**Benefits of Contexts:**

* Improved scalability: By partitioning events, you can distribute workload across multiple consumers, enhancing performance.
* Focused processing: Consumers handle only events relevant to their context, leading to more efficient processing.
* Modular design: Contexts promote modularity in your event-driven architecture by enabling clear separation of concerns.

By effectively utilizing contexts, you can streamline event handling within your Evento applications. Contexts allow for efficient partitioning of event streams, leading to focused processing and improved scalability in your event-driven system.
