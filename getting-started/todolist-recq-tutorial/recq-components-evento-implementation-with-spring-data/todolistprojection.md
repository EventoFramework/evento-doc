# TodoListProjection

To handle Query Messages we need to implement a Projection.&#x20;

In EVento Framework a projection is a standard class annotated with @Projection (com.evento.common.modeling.annotations.component.Projection). It contains Query Handlers, methods annotated with `@QueryHandler (com.evento.common.modeling.annotations.handler.QueryHandler)` with the Query as a parameter and returning a Single or a Multiple of a particular View.

```java
import com.eventoframework.demo.todo.api.todo.query.TodoListListItemViewSearchQuery;
import com.eventoframework.demo.todo.api.todo.query.TodoListViewFindByIdentifierQuery;
import com.eventoframework.demo.todo.api.todo.view.TodoListListItemView;
import com.eventoframework.demo.todo.api.todo.view.TodoListView;
import com.eventoframework.demo.todo.query.model.TodoList;
import com.eventoframework.demo.todo.query.model.TodoListRepository;
import com.evento.common.modeling.annotations.component.Projection;
import com.evento.common.modeling.annotations.handler.QueryHandler;
import com.evento.common.modeling.messaging.query.Multiple;
import com.evento.common.modeling.messaging.query.Single;
import org.springframework.data.domain.PageRequest;

@Projection()
public class TodoListProjection {

    private final TodoListRepository repository;

    public TodoListProjection(TodoListRepository repository) {
        this.repository = repository;
    }

    @QueryHandler
    public Single<TodoListView> handle(TodoListViewFindByIdentifierQuery query) {
        return Single.of(repository.findById(query.getIdentifier()).map(TodoList::toView).orElseThrow());
    }

    @QueryHandler
    public Multiple<TodoListListItemView> handle(TodoListListItemViewSearchQuery query) {
        return Multiple.of(repository.search(
                        "%" + query.getNameLike() + "%",
                        PageRequest.of(query.getPage(),
                                query.getSize()))
                .map(TodoList::toListItemView).toList());
    }
}
```
