# Expose the RECQ architecture with Spring Web

The last level of the layered architecture after the service, implemented by a RECQ Invoker, is the Controller.

The main goal of a controller is let user interact with the software core logic using a particular protocol or interface.

In this tutorial, we are going to expose our System with a REST Interface implemented by a Spring Controller.

```java
import com.eventoframework.demo.todo.api.todo.view.TodoListListItemView;
import com.eventoframework.demo.todo.api.todo.view.TodoListView;
import com.eventoframework.demo.todo.service.invoker.TodoListInvoker;
import com.evento.application.EventoBundle;
import com.eventoframework.demo.todo.web.dto.CreatedResponse;
import com.eventoframework.demo.todo.web.dto.TodoCreateRequest;
import com.eventoframework.demo.todo.web.dto.TodoListCreateRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Collection;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/todo-list")
public class TodoListController {

    private final TodoListInvoker todoListInvoker;

    public TodoListController(EventoBundle eventoBundle) {
        // Instantiate the invoker
        todoListInvoker = eventoBundle.getInvoker(TodoListInvoker.class);
    }

    @GetMapping("/")
    public CompletableFuture<ResponseEntity<Collection<TodoListListItemView>>> searchTodoList(
           @RequestParam(defaultValue = "") String nameLike, @RequestParam(defaultValue = "0") int page
    ) {
        return todoListInvoker
                .searchTodoList(nameLike, page)
                .thenApply(ResponseEntity::ok);
    }

    @GetMapping("/{identifier}")
    public CompletableFuture<ResponseEntity<TodoListView>> findTodoListByIdentifier(
            @PathVariable String identifier) {
        return todoListInvoker
                .findTodoListByIdentifier(identifier)
                .thenApply(ResponseEntity::ok);
    }

    @PostMapping("/")
    public ResponseEntity<CreatedResponse> createTodoList(
            @RequestBody TodoListCreateRequest request, @RequestHeader(name = "Authorization") String user) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(new CreatedResponse(
                        todoListInvoker.createTodoList(request.getName(), user)
                ));
    }


    @DeleteMapping("/{identifier}")
    public ResponseEntity<Void> deleteTodoList(
            @PathVariable String identifier,
            @RequestHeader(name = "Authorization") String user) {
        todoListInvoker.deleteTodoList(identifier, user);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{identifier}/todo/")
    public ResponseEntity<CreatedResponse> addTodo(
            @PathVariable String identifier,
            @RequestBody TodoCreateRequest request,
            @RequestHeader(name = "Authorization") String user) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new CreatedResponse(
                        todoListInvoker.addTodo(identifier, request.getContent(), user)
                ));
    }

    @DeleteMapping("/{identifier}/todo/{todoIdentifier}")
    public ResponseEntity<Void> removeTodo(
            @PathVariable String identifier,
            @PathVariable String todoIdentifier,
            @RequestHeader(name = "Authorization") String user) {
        todoListInvoker.removeTodo(identifier, todoIdentifier, user);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/{identifier}/todo/{todoIdentifier}")
    public ResponseEntity<Void> checkTodo(
            @PathVariable String identifier,
            @PathVariable String todoIdentifier,
            @RequestHeader(name = "Authorization") String user) {
        todoListInvoker.checkTodo(identifier, todoIdentifier, user);
        return ResponseEntity.accepted().build();
    }
}
```

### DTOs

```java
import lombok.Data;

@Data
public class TodoListCreateRequest {
    private String name;
}
```

```java
import lombok.Data;

@Data
public class TodoCreateRequest {
    private String content;
}
```

```java
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class CreatedResponse {
    private String identifier;
}
```

