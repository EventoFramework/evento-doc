---
description: Implementing the Domain Change Requests Actions
---

# Domain Commands

First, let's implement all the Domain Commands: domain commands are all commands related to an [Aggregate](../../../recq-patterns/recq-component-pattern/aggregate.md) and generating events after the approval.

In Evento Framework every Domain Command implement the class `com.evento.common.modeling.messaging.payload.DomainCommand` and needs the `getAggregateId()` method implementation. Thath method returns the **Unique Aggregate Identifier** used to compute the [Aggregate State](../../../evento-framework/component/aggregate/aggregate-state.md) of the Event Sourcing Pattern. Then you have to specify every single required information as a field.

{% hint style="danger" %}
Every single AggregateId in the System must be different you cannot use the same ID in different aggregate Types.
{% endhint %}

{% hint style="info" %}
Usually, the Resource Identifier (in this case the TodoList Id) is used as an aggregate identifier, and, during the generation, a prefix to identify the aggregate type.
{% endhint %}

```java
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainCommand;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListCreateCommand extends DomainCommand {
    
    // The TodoList identifier
    private String identifier;
    // The TodoList Name
    private String name;
    
    @Override
    public String getAggregateId() {
        return identifier;
    }
}
```

```java
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainCommand;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListDeleteCommand  extends DomainCommand {

    // Identifier of the TodoList to delete
    private String identifier;

    @Override
    public String getAggregateId() {
        return identifier;
    }
}
```

```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainCommand;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListAddTodoCommand extends DomainCommand {

    // Identifier of the TodoList to update
    private String identifier;
    // Identifier of the To-do to delete
    private String todoIdentifier;
    // The To-do content
    private String content;
    @Override
    public String getAggregateId() {
        return identifier;
    }
}
```

```java
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainCommand;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListRemoveTodoCommand extends DomainCommand {

    // Identifier of the TodoList to update
    private String identifier;
    // Identifier of the To-do to remove
    private String todoIdentifier;
    @Override
    public String getAggregateId() {
        return identifier;
    }
}
```

```java
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.DomainCommand;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListCheckTodoCommand extends DomainCommand {

    // Identifier of the TodoList to update
    private String identifier;
    // Identifier of the To-do to check
    private String todoIdentifier;
    @Override
    public String getAggregateId() {
        return identifier;
    }
}
```
