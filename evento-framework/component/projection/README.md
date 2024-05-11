# @Projection

In the realm of CQRS (Command Query Responsibility Segregation), projections play a crucial role in defining the read model for your application. This chapter explores the `@Projection` annotation within Evento and delves into how it's used to create projections that serve as the source of data for queries.

#### Understanding Projections

The `@Projection` annotation marks a class as a projection within your Evento application. Projections are responsible for one and only task:

1. **Query Handling:** Projections handle queries by retrieving data from the projection state stored in the database and transforming it into a format suitable for the query response.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Component
public @interface Projection {
}
```

Here's a breakdown of the `@Projection` annotation:

* **`@Retention(RetentionPolicy.RUNTIME)`:** This ensures that the annotation information is retained at runtime, allowing Evento to access it during application execution.
* **`@Target(ElementType.TYPE)`:** This specifies that the annotation can only be applied to class declarations.
* **`@Component`:** This indicates that the annotated class is a component within the Evento framework.

#### How Projections Work

Projections leverage the `@QueryHandler` annotation to define methods that handle incoming queries. These query handler methods typically follow this pattern:

1. **Query Reception:** The query handler method receives a specific query object as input.
2. **Data Retrieval:** The method retrieves relevant data from the projection state stored in the database. This might involve querying a repository or accessing cached data.
3. **Data Transformation (Optional):** Depending on the query requirements, the retrieved data might need to be transformed or enriched before returning it as part of the response.
4. **Query Response Construction:** The method constructs a response object containing the data retrieved and transformed as needed.

**Example: Projection in Action:**

```java
@Projection
public class DemoProjection {

    private final DemoRepository repository;

    public DemoProjection(DemoRepository repository) {
        this.repository = repository;
    }

    @QueryHandler
    Single<DemoView> query(DemoViewFindByIdQuery query, QueryMessage<DemoViewFindByIdQuery> queryMessage) {
        Utils.logMethodFlow(this, "query", query, "BEGIN");
        var result = repository.findById(query.getDemoId())
                .filter(d -> d.getDeletedAt() == null)
                .map(Demo::toDemoView).orElseThrow();
        result.setDemoId(query.getDemoId());
        Utils.logMethodFlow(this, "query", query, "END");
        return Single.of(result);
    }

    @QueryHandler
    Multiple<DemoView> query(DemoViewFindAllQuery query) {
        Utils.logMethodFlow(this, "query", query, "BEGIN");
        var result = repository.findAll().stream()
                .filter(d -> d.getDeletedAt() == null)
                .map(Demo::toDemoView).toList();
        Utils.logMethodFlow(this, "query", query, "END");
        return Multiple.of(result);
    }

    @QueryHandler
    Single<DemoRichView> queryRich(DemoRichViewFindByIdQuery query) {
        Utils.logMethodFlow(this, "query", query, "BEGIN");
        var result = repository.findById(query.getDemoId())
                .map(Demo::toDemoRichView).orElseThrow();
        Utils.logMethodFlow(this, "query", query, "END");
        return Single.of(result);
    }


    @QueryHandler
    Multiple<DemoRichView> queryRich(DemoRichViewFindAllQuery query) {
        Utils.logMethodFlow(this, "query", query, "BEGIN");
        var result = repository.findAll().stream().map(Demo::toDemoRichView).toList();
        Utils.logMethodFlow(this, "query", query, "END");
        return Multiple.of(result);
    }
}
```

The provided code example showcases a `DemoProjection` class:

* The class is annotated with `@Projection`, indicating it's a projection.
* It has a constructor that injects a `DemoRepository` dependency.
* It defines four `@QueryHandler` methods:
  * Two methods handle `DemoViewFindByIdQuery` and `DemoViewFindAllQuery` for retrieving basic `DemoView` objects.
  * Two other methods handle `DemoRichViewFindByIdQuery` and `DemoRichViewFindAllQuery` for retrieving richer `DemoRichView` objects.
* Each query handler method retrieves data from the `DemoRepository` based on the query type, applies any necessary transformations, and constructs the corresponding response object (either `Single` or `Multiple` depending on the query type).

**Key Points:**

* Projections serve as the bridge between the domain events (representing the write model) and the queryable data (the read model).
* `@QueryHandler` methods within projections are responsible for handling queries and constructing appropriate responses.
* Projections play a vital role in ensuring efficient retrieval of data for queries within a CQRS architecture.

In the next chapter, we'll explore the concept of projectors and how they work in tandem with projections to maintain a consistent read model.
