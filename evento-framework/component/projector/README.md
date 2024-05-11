---
description: Materializing Domain State
---

# @Projector

In the realm of CQRS (Command Query Responsibility Segregation), projectors play a crucial role in bridging the gap between the write model (domain events) and the read model (queryable data). This chapter dives into the concept of projectors within Evento and explores how they are used to materialize the current state of your domain from domain events.

#### Understanding Projectors

The `@Projector` annotation identifies a class as a projector within your Evento application. Projectors are responsible for handling domain events published as a result of command execution and updating a corresponding projection state stored in a database. Essentially, they translate domain events into a format suitable for querying and retrieval.

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Component
public @interface Projector {
    /**
     * Returns the version of the Projector.
     *
     * @return the version of the Projector
     */
    int version();
}
```

Here's a breakdown of the `@Projector` annotation:

* **`@Retention(RetentionPolicy.RUNTIME)`:** This ensures that the annotation information is retained at runtime, allowing Evento to access it during application execution.
* **`@Target(ElementType.TYPE)`:** This specifies that the annotation can only be applied to class declarations.
* **`@Component`:** This indicates that the annotated class is a component within the Evento framework.

The `@Projector` annotation also includes a `version` parameter:

* **`version` (int):** This parameter specifies the version of the projector. This versioning mechanism becomes crucial when significant changes are made to the projection logic. A new version allows Evento to potentially recompute the projection state based on the revised logic.

#### How Projectors Work

Projectors rely on the `@EventHandler` annotation to define methods that react to specific domain events. These event handler methods typically follow this pattern:

1. **Event Reception:** The event handler method receives a domain event object as input.
2. **Projection Update Logic:** Based on the received event, the handler method updates the corresponding projection state in the database. This might involve creating a new entry, modifying existing data, or potentially deleting data from the projection.
3. **Optional Additional Logic:** In some scenarios, projectors might perform additional tasks like logging or sending notifications after updating the projection state.

**Example: Projector in Action**

```java
import com.evento.common.messaging.gateway.QueryGateway;
import com.evento.common.modeling.annotations.component.Projector;
import com.evento.common.modeling.annotations.handler.EventHandler;
import com.evento.common.modeling.messaging.message.application.EventMessage;
import com.evento.demo.api.event.DemoCreatedEvent;
import com.evento.demo.api.event.DemoDeletedEvent;
import com.evento.demo.api.event.DemoUpdatedEvent;
import com.evento.demo.api.utils.Utils;
import com.evento.demo.query.domain.Demo;
import com.evento.demo.query.domain.DemoRepository;

import java.time.Instant;

@Projector(version = 3)
public class DemoProjector {

    private final DemoRepository demoRepository;

    public DemoProjector(DemoRepository demoRepository) {
       this.demoRepository = demoRepository;
    }

    @EventHandler
    void on(DemoCreatedEvent event, QueryGateway queryGateway, EventMessage<?> eventMessage) {
       Utils.logMethodFlow(this, "on", event, "BEGIN");
       var now = Instant.now();
       demoRepository.save(new Demo(event.getDemoId(), event.getName(),
             event.getValue(), now, now, null));
       Utils.logMethodFlow(this, "on", event, "END");
    }

    @EventHandler
    void on(DemoUpdatedEvent event) {
       Utils.logMethodFlow(this, "on", event, "BEGIN");
       var now = Instant.now();
       demoRepository.findById(event.getDemoId()).ifPresent(d -> {
          d.setName(event.getName());
          d.setValue(event.getValue());
          d.setUpdatedAt(Instant.now());
          demoRepository.save(d);
       });
       Utils.logMethodFlow(this, "on", event, "END");

    }

    @EventHandler
    void on(DemoDeletedEvent event) {
       Utils.logMethodFlow(this, "on", event, "BEGIN");
       demoRepository.findById(event.getDemoId()).ifPresent(d -> {
          d.setDeletedAt(Instant.now());
          demoRepository.save(d);
       });
       Utils.logMethodFlow(this, "on", event, "END");

    }
}
```

The provided code example showcases a `DemoProjector` class:

* The class is annotated with `@Projector(version = 3)`, indicating its version.
* It has a constructor that injects a `DemoRepository` dependency.
* Three `@EventHandler` methods handle `DemoCreatedEvent`, `DemoUpdatedEvent`, and `DemoDeletedEvent` respectively.
* Each event handler method updates the `Demo` projection object in the database based on the information contained in the corresponding domain event.

**Key Points:**

* Projectors provide a mechanism to materialize the current state of your domain from the stream of domain events.
* The versioning mechanism associated with projectors allows for flexibility when evolving the projection logic.
* Projectors work hand-in-hand with query repositories to enable efficient retrieval of domain data for querying purposes.

**In the next chapter, we'll explore how projectors integrate with the consumer state store within Evento to manage the overall event processing flow.**
