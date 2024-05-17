---
description: System State Change Events
---

# Domain Events

For each Domain Command, we need to create a Domain Event representing the System Change State.

Domain Events in Evento Framework are implemented by extending the abstract class `com.evento.common.modeling.messaging.payload.DomainEvent`. This class has no required method to implement but extends the generic Event class that includes a property called _Context_ which we will discuss later.

{% hint style="info" %}
Use Past verbs to indicate Events and Present for Commands.

Events can contain more information than the relative command for optimization purposes. (See TodoListTodoCheckedEvent)
{% endhint %}

Usually, each event has a very similar name to the relative command but with an ending Event and a Partial verbal time.

```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainEvent;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListCreatedEvent extends DomainEvent {

    private String identifier;
    private String content;
}
```

```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainEvent;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListDeletedEvent extends DomainEvent {

    private String identifier;
}
```

```java
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainCommand;
import com.evento.common.modeling.messaging.payload.DomainEvent;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListTodoAddedEvent extends DomainEvent {

    private String identifier;
    private String todoIdentifier;
    private String content;
}
```

```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainEvent;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListTodoCheckedEvent extends DomainEvent {

    private String identifier;
    private String todoIdentifier;
    // Communicate if all Todos inside this TodoList are checked with this check
    private boolean allChecked;
}
```

```java
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainCommand;
import com.evento.common.modeling.messaging.payload.DomainEvent;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListTodoRemovedEvent extends DomainEvent {

    private String identifier;
    private String todoIdentifier;
}
```
