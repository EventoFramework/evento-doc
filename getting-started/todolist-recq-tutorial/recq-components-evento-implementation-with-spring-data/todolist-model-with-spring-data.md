# TodoList Model with Spring Data

Usually, we start building the Domain Fisical Representation from The Query Point of View. One particular characteristic of RECQ Architecture is the application of the Database-per-query pattern where you design entire databases only to fulfil a Query most efficiently. In order to do that we need to explore all the Queries to define indexes and database paradigms that handle better the request and analyse Views to define the required fields.

### Model

In this tutorial, we have chosen to use Spring Data JPA and a relational database to store objects, but we are gonna to implement the Document Paradigm to represent OneToMany Relations.

So, we can start defining the Todo object and inside of it the mapper method toView() that returns the Entity as RECQ View Payload:

```java
import com.eventoframework.demo.todo.api.todo.view.TodoView;
import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.ZonedDateTime;

@Embeddable
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class Todo {
    private String identifier;
    private String content;
    private String createdBy;
    private String completedBy;
    private ZonedDateTime createdAt;
    private ZonedDateTime completedAt;

    public TodoView toView() {
        return new TodoView(
                identifier,
                content,
                completedAt != null,
                createdBy,
                completedBy,
                createdAt,
                completedAt
        );
    }
}
```

Then the parent object, the TodoList with two different mappers, one for the List Representation and one for the detailed.

```java
import com.eventoframework.demo.todo.api.todo.view.TodoListListItemView;
import com.eventoframework.demo.todo.api.todo.view.TodoListView;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class TodoList {
    @Id
    private String identifier;
    private String name;
    private String createdBy;
    private String updatedBy;
    private ZonedDateTime createdAt;
    private ZonedDateTime updatedAt;
    @ElementCollection(fetch=FetchType.EAGER)
    private List<Todo> todos;

    public TodoListView toView() {
        return new TodoListView(getIdentifier(),
                getName(),
                new ArrayList<>(getTodos().stream().map(Todo::toView).toList()),
                getCreatedBy(),
                getUpdatedBy(),
                getCreatedAt(),
                getUpdatedAt());
    }

    public TodoListListItemView toListItemView() {
        return new TodoListListItemView(getIdentifier(), getName());
    }

}
```

### Repository

Once the model is properly implemented, we can define the Repository to access database Data and also adding specific methods to answer the proper Queries.

```java
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface TodoListRepository extends JpaRepository<TodoList, String> {
    @Query("select t from TodoList t where t.name like ?1")
    Page<TodoList> search(String query,
                          Pageable pageable);
}
```
