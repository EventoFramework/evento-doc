---
description: The ways that we use to see your System State.
---

# Views

Before asking data from the System we need to know the resulting structure, that's why we need to implement Objects representing data in a formal way.

It constantly happens that the same Domain or Aggregate could be represented in multiple ways based on the request purpose, such as in our case, we have two requirements:

* The list of all TodoList
* The single TodoList

In the first case, we only need generic information to explore the situation and maybe peek at a particular list, in the second case, probably we need a more specific representation.

This separation helps us to optimize requests, traffic and workloads.

```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.View;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListListItemView implements View {
    private String identifier;
    private String name;
}
```

```java
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.View;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.ZonedDateTime;
import java.util.ArrayList;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoListView implements View {
    private String identifier;
    private String name;
    private ArrayList<TodoView> todos;
    private String createdBy;
    private String updatedBy;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
}
```

```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import com.evento.common.documentation.Domain;
import com.evento.common.modeling.messaging.payload.View;

import java.time.ZonedDateTime;

@Domain(name = "TodoList")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoView implements View {
    private String identifier;
    private String content;
    private boolean completed;
    private String createdBy;
    private String completedBy;
    private ZonedDateTime createdAt;
    private ZonedDateTime completedAt;
}
```
