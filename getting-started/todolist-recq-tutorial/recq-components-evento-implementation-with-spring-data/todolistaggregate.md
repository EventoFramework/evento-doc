# TosoListAggregate

### Aggregate State

To implement properly an Aggregate with Evento Framework we need first to define the Aggregate State. To do this we need to create a specific class for each Aggregate extending the `com.evento.common.modeling.state.AggregateState` class.

```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.modeling.state.AggregateState;

import java.util.HashMap;

@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListAggregateState extends AggregateState {
    private HashMap<String, Boolean> todos;
}
```

As state, we are gonna to use a Map Structure representing the todos contained in the TodoList with the boolean indication for checked/unlocked.

## Aggregate

In evento Framework, an Aggregate is implemented with a simple class decorated with the annotation @Aggregate (com.evento.common.modeling.annotations.component.Aggregate).

The Aggregate class will contain two classes of methods:&#x20;

* `handle(c: Command): Event` - The AggregateCommandHandlers handle Domain Commands and return a System State Changed Event (a Domain Event) after a validation of the command given the aggregate state.
* `on(e: Event): AggregateState` - The EventSourcingHandlers are used to compute the aggregate state given an event stream.

In order to properly implement these handlers you need to use the proper annotation:&#x20;

* `com.evento.common.modeling.annotations.handler.AggregateCommandHandler`
* `com.evento.common.modeling.annotations.handler.EventSourcingHandler`

&#x20;Each aggregate instance represents a unique object with its lifecycle (born, live, dead).

To create a new Aggregate for a Domain we need to define a command that gives birth to that specific instance, to indicate with the command handler is used to generate a new instance there is the `init` parameter that must be sat as `true`;

{% hint style="info" %}
We suggest implementing the Command Handler and the Event Handler related to a particular action together and one after the other as in the example below to improve readability.
{% endhint %}

To indicate the Aggregate dead you need to use the EventSourcingHandler and mark the state as deleted with the `setDeleted(b: Boolean)` method.

```java
import com.evento.common.modeling.annotations.component.Aggregate;
import com.evento.common.modeling.annotations.handler.AggregateCommandHandler;
import com.evento.common.modeling.annotations.handler.EventSourcingHandler;
import com.eventoframework.demo.todo.api.todo.command.*;
import com.eventoframework.demo.todo.api.todo.event.*;
import org.springframework.util.Assert;

import java.util.HashMap;

@Aggregate
public class TodoListAggregate {

    @AggregateCommandHandler(init = true)
    public TodoListCreatedEvent handle(TodoListCreateCommand command){
        // Validation
        Assert.isTrue(command.getAggregateId() != null,
                "Error: Todo Id is null");
        Assert.isTrue(command.getName() != null && !command.getName().isBlank(),
                "Error: Content is empty");
        // Command is valid
        return new TodoListCreatedEvent(command.getIdentifier(), command.getName());
    }

    @EventSourcingHandler
    public TodoListAggregateState on(TodoListCreatedEvent event){
        var state = new TodoListAggregateState();
        state.setTodos(new HashMap<>());
        return state;
    }

    @AggregateCommandHandler
    public TodoListDeletedEvent handle(TodoListDeleteCommand command, TodoListAggregateState state){
        // Validation
        Assert.isTrue(state.getTodos().values().stream().noneMatch(a -> a),
                "Error: List contains a checked todo");

        // Command is valid
        return new TodoListDeletedEvent(command.getIdentifier());
    }

    @EventSourcingHandler
    public void on(TodoListDeletedEvent event, TodoListAggregateState state){
        state.setDeleted(true);
    }

    @AggregateCommandHandler
    public TodoListTodoAddedEvent handle(TodoListAddTodoCommand command, TodoListAggregateState state){
        // Command Validation
        Assert.isTrue(command.getTodoIdentifier() != null && !command.getTodoIdentifier().isBlank(),
                "Error: Invalid todo identifier");
        Assert.isTrue(command.getContent() != null && !command.getContent().isBlank(),
                "Error: Invalid todo content");
        // State Validation
        Assert.isTrue(!state.getTodos().containsKey(command.getTodoIdentifier()),
                "Error: Todo already present");
        Assert.isTrue(state.getTodos().size() < 5,
                "Error: Todo list is full");
        // Command is valid
        return new TodoListTodoAddedEvent(
                command.getIdentifier(),
                command.getTodoIdentifier(),
                command.getContent());
    }

    @EventSourcingHandler
    public void on(TodoListTodoAddedEvent event, TodoListAggregateState state){
        state.getTodos().put(event.getTodoIdentifier(), false);
    }

    @AggregateCommandHandler
    public TodoListTodoRemovedEvent handle(TodoListRemoveTodoCommand command, TodoListAggregateState state){
        // Validation
        Assert.isTrue(state.getTodos().containsKey(command.getTodoIdentifier()),
                "Error: Todo not present");
        Assert.isTrue(!state.getTodos().get(command.getTodoIdentifier()),
                "Error: Todo already checked");
        // Command is valid
        return new TodoListTodoRemovedEvent(
                command.getIdentifier(),
                command.getTodoIdentifier());
    }

    @EventSourcingHandler
    public void on(TodoListTodoRemovedEvent event, TodoListAggregateState state){
        state.getTodos().remove(event.getTodoIdentifier());
    }

    @AggregateCommandHandler
    public TodoListTodoCheckedEvent handle(TodoListCheckTodoCommand command, TodoListAggregateState state){
        // Validation
        Assert.isTrue(state.getTodos().containsKey(command.getTodoIdentifier()),
                "Error: Todo not present");
        Assert.isTrue(!state.getTodos().get(command.getTodoIdentifier()),
                "Error: Todo already checked");
        // Command is valid
        return new TodoListTodoCheckedEvent(
                command.getIdentifier(),
                command.getTodoIdentifier(),
                state.getTodos().values().stream().allMatch(b -> b));
    }

    @EventSourcingHandler
    public void on(TodoListTodoCheckedEvent event, TodoListAggregateState state){
        state.getTodos().put(event.getTodoIdentifier(), true);
    }
}
```
