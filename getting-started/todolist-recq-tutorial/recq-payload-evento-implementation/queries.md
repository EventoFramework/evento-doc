---
description: Implementing the Data Retrieval Actions
---

# Queries

All actions that are a Data Request by the System are mapped as Query Messages.

A Query in Evento Framework implements the `com.evento.common.modeling.messaging.payload.Query` class, that requires a Parameter indicating the return type: a Single or a Multiple of View extending classes.

{% hint style="info" %}
I suggest implementing Queries and Views at the same time in order to properly map data requests and structure.
{% endhint %}

In our requirements, we got two specifications: the list all and the find one.&#x20;

```java
import com.eventoframework.demo.todo.api.todo.view.TodoListListItemView;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.Query;
import com.evento.common.modeling.messaging.query.Multiple;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListListItemViewSearchQuery 
        extends Query<Multiple<TodoListListItemView>> {
    // A like filter for the TodoList name
    private String nameLike;
    // Pagination infos
    private int page;
    private int size;
}
```

In the above case, we have used the `com.evento.common.modeling.messaging.query.Multiple` type for return because we are going to return a Collection of `TodoListListItemView.`

```java
import com.eventoframework.demo.todo.api.todo.view.TodoListView;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.Query;
import com.evento.common.modeling.messaging.query.Single;
@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListViewFindByIdentifierQuery 
        extends Query<Single<TodoListView>> {
    private String identifier;
}
```

For the find by Id case, we are gonna return only one TodoListView object so we need to use the `com.evento.common.modeling.messaging.query.Single` class as Query return type.
