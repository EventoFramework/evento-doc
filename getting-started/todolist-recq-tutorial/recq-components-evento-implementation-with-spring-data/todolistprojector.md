# TodoListProjector

After the proper definition of the Event Generation in our System and the Model/Repository Layers, we can start to build our Projector, also known as, the domain materializer. The main goal of this component is to store in a database a particular View of the System State.

In Evento Framework a Projector is a simple class annotated with `@Projector (com.evento.common.modeling.annotations.component.Projector)`. This annotation requires a parameter called version that indicate the materialization version in order to recreate the database or change the structure. A complete description of a projector can be found in the [Projector Chapter](../../../evento-framework/component/projector/).

```java
import com.evento.common.modeling.messaging.message.application.Metadata;
import com.eventoframework.demo.todo.api.todo.event.*;
import com.eventoframework.demo.todo.query.model.Todo;
import com.eventoframework.demo.todo.query.model.TodoList;
import com.eventoframework.demo.todo.query.model.TodoListRepository;
import com.evento.common.modeling.annotations.component.Projector;
import com.evento.common.modeling.annotations.handler.EventHandler;
import com.evento.common.modeling.messaging.message.application.EventMessage;

import java.time.Instant;
import java.time.ZoneId;
import java.util.ArrayList;

@Projector(version = 1)
public class TodoListProjector{

    private final TodoListRepository repository;


    public TodoListProjector(TodoListRepository repository) {
        this.repository = repository;
    }

    @EventHandler
    public void on(TodoListCreatedEvent event, Metadata metadata, Instant timestamp) {
        repository.save(new TodoList(
                event.getIdentifier(),
                event.getContent(),
                metadata.get("user"),
                null,
                timestamp.atZone(ZoneId.systemDefault()),
                null,
                new ArrayList<>()
        ));
    }

    @EventHandler
    public void on(TodoListDeletedEvent event, EventMessage<TodoListCreatedEvent> message) {
        repository.delete(repository.findById(event.getIdentifier()).orElseThrow());
    }

    @EventHandler
    public void on(TodoListTodoAddedEvent event, Metadata metadata, Instant timestamp) {
        var list = repository.findById(event.getIdentifier()).orElseThrow();
        var td = new Todo(
                event.getTodoIdentifier(),
                event.getContent(),
                metadata.get("user"),
                null,
                timestamp.atZone(ZoneId.systemDefault()),
                null
        );
        list.getTodos().add(td);
        list.setUpdatedAt(td.getCreatedAt());
        list.setUpdatedBy(td.getCreatedBy());
        repository.save(list);
    }

    @EventHandler
    public void on(TodoListTodoRemovedEvent event, Metadata metadata, Instant timestamp) {
        var list = repository.findById(event.getIdentifier()).orElseThrow();
        list.getTodos().removeIf(t -> event.getTodoIdentifier().equals(t.getIdentifier()));
        list.setUpdatedAt(timestamp.atZone(ZoneId.systemDefault()));
        list.setUpdatedBy(metadata.get("user"));
        repository.save(list);
    }

    @EventHandler
    public void on(TodoListTodoCheckedEvent event, Metadata metadata, Instant timestamp) {
        var list = repository.findById(event.getIdentifier()).orElseThrow();
        var td = list.getTodos().stream().filter(t -> event.getTodoIdentifier().equals(t.getIdentifier())).findFirst().orElseThrow();
        td.setCompletedAt(timestamp.atZone(ZoneId.systemDefault()));
        td.setCompletedBy(metadata.get("user"));
        list.setUpdatedAt(td.getCompletedAt());
        list.setUpdatedBy(td.getCompletedBy());
        repository.save(list);
    }
}
```
