# TodoList Invoker

In the end, we need to implement the Invoker, the bridge component between the standard application and the RECQ architecture.

An Invoker is a class annotated with `@Invoker` (`com.evento.common.modeling.annotations.component.Invoker`) and extending the `com.evento.application.proxy.InvokerWrapper` class. An invoker contains methods annotated with `@InvocationHandler` (`com.evento.common.modeling.annotations.handler.InvocationHandler`) used to implement business logic using the Command Gateway and the Query Gateway that you can access with `getCommandGateway()` and `getQueryGateway()` methods.

```java
import com.eventoframework.demo.todo.api.todo.command.*;
import com.eventoframework.demo.todo.api.todo.query.TodoListListItemViewSearchQuery;
import com.eventoframework.demo.todo.api.todo.query.TodoListViewFindByIdentifierQuery;
import com.eventoframework.demo.todo.api.todo.view.TodoListListItemView;
import com.eventoframework.demo.todo.api.todo.view.TodoListView;
import com.evento.application.proxy.InvokerWrapper;
import com.evento.common.modeling.annotations.component.Invoker;
import com.evento.common.modeling.annotations.handler.InvocationHandler;
import com.evento.common.modeling.messaging.message.application.Metadata;
import com.evento.common.modeling.messaging.query.Multiple;
import com.evento.common.modeling.messaging.query.Single;

import java.util.Collection;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@Invoker
public class TodoListInvoker extends InvokerWrapper {

    @InvocationHandler
    public String createTodoList(String name, String user){
        var identifier = "TDLS_" + UUID.randomUUID();
        getCommandGateway().send(new TodoListCreateCommand(identifier, name), toUserMetadata(user)).get();
        return identifier;
    }

    @InvocationHandler
    public void deleteTodoList(String identifier, String user){
        getCommandGateway().send(new TodoListDeleteCommand(identifier), toUserMetadata(user)).get();
    }
    
    @InvocationHandler
    public String addTodo(String identifier, String content, String user){
        var todoIdentifier = "TODO_" + UUID.randomUUID();
        getCommandGateway().send(new TodoListAddTodoCommand(identifier, todoIdentifier, content), toUserMetadata(user)).get();
        return todoIdentifier;
    }
    
    @InvocationHandler
    public void checkTodo(String identifier, String todoIdentifier, String user){
        getCommandGateway().send(new TodoListCheckTodoCommand(identifier, todoIdentifier), toUserMetadata(user)).get();
    }
    
    @InvocationHandler
    public void removeTodo(String identifier, String todoIdentifier, String user){
        getCommandGateway().send(new TodoListRemoveTodoCommand(identifier, todoIdentifier), toUserMetadata(user)).get();
    }

    @InvocationHandler
    public CompletableFuture<TodoListView> findTodoListByIdentifier(String identifier){
        return getQueryGateway().query(new TodoListViewFindByIdentifierQuery(identifier)).thenApply(Single::getData);
    }

    @InvocationHandler
    public CompletableFuture<Collection<TodoListListItemView>> searchTodoList(String nameLike, int page){
        return getQueryGateway().query(new TodoListListItemViewSearchQuery(nameLike, page, 15))
                .thenApply(Multiple::getData);
    }

    private Metadata toUserMetadata(String user) {
        var m = new Metadata();
        m.put("user", user);
        return m;
    }
}
```

{% hint style="info" %}
An invoker implements the Service Layer of the Layered Architecture, also, this separation gives the correct level of abstraction when you need to interact with other java frameworks or libraries.
{% endhint %}
