# @QueryHandler

In the realm of CQRS (Command Query Responsibility Segregation), projections play a crucial role in serving data for queries. This chapter dives into the `@QueryHandler` annotation used within projections to define methods that handle incoming queries efficiently.

#### Understanding `@QueryHandler`

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Handler
public @interface QueryHandler {
}
```

The `@QueryHandler` annotation identifies a method within your projection class as a query handler. This method is responsible for processing a specific query object, retrieving relevant data from the projection state, and constructing the corresponding response.

Here's a breakdown of the annotation's definition:

* **`@Retention(RetentionPolicy.RUNTIME)`:** Ensures the annotation information is retained at runtime, allowing Evento to discover and execute these methods when queries arrive.
* **`@Target(ElementType.METHOD)`:** Specifies that the annotation can only be applied to method declarations within your projection class.
* **`@Handler` (Optional):** In some frameworks like Evento, `@QueryHandler` might inherit from a base annotation like `@Handler` for consistency in marking different handler types.

#### Structure of a `@QueryHandler` Method

A well-structured `@QueryHandler` method typically adheres to the following pattern:

1. **Query Object as First Parameter:** The first parameter of the method must be a subtype of the `Query` class representing the specific type of query being handled (e.g., `DemoViewFindByIdQuery`).
2. **Optional Additional Parameters:** Depending on your specific needs, you might include additional parameters like:
   * `QueryMessage<Query>` (Optional): This provides access to details about the received query message, including metadata and timestamp.
   * `QueryGateway` (Optional): This allows implementing the federated query pattern within your query handler (discussed in a later chapter).
   * `Metadata` (Optional): This represents metadata associated with the query (often already included in the `QueryMessage` object).
   * `Instant` (Optional): This represents the timestamp of the query message.
3. **Single or Multiple Return Type:** The return type of the `@QueryHandler` method can be either `Single<View>` or `Multiple<View>`.
   * `Single<View>`: Used for queries that expect a single response object of a specific view type (e.g., `DemoView`).
   * `Multiple<View>`: Used for queries that expect a collection of view objects of a specific type (e.g., retrieving a list of `DemoView` objects).

{% hint style="warning" %}
The `QueryGateway` within Evento empowers you to implement the federated query pattern, fetching data from various services to construct a comprehensive response. However, it's crucial to be mindful of eventual consistency when using this approach, especially when joining data from multiple sources.

Here's why eventual consistency can lead to inconsistencies:

* **Asynchronous Updates:** Event sourcing systems often rely on asynchronous processing of events. This means that updates to different services might not occur instantaneously.
* **Data Latency:** There might be a slight delay between the time an event is processed in one service and the time the corresponding update propagates to its database.

**Impact on Federated Queries:**

When you use `QueryGateway` to join data from multiple services with eventual consistency, there's a possibility of encountering inconsistencies in the joined results. You might retrieve data that reflects different points in time across the services involved.

**Example Scenario:**

Imagine a scenario where you use `QueryGateway` to fetch a user's profile information (from one service) and their recent order details (from another service) to display a combined view. Due to eventual consistency, the user's profile data might be updated immediately after placing an order, but the order details might not be reflected in the other service yet. This could result in the user profile showing the updated information, while the order details section remains empty.
{% endhint %}

**Example: `@QueryHandler` in Action**

```java
@QueryHandler
Single<DemoView> query(DemoViewFindByIdQuery query,
                       QueryMessage<DemoViewFindByIdQuery> queryMessage,
                       QueryGateway queryGateway,
                       Metadata metadata,
                       Instant instant) {
    Utils.logMethodFlow(this, "query", query, "BEGIN");
    var result = repository.findById(query.getDemoId())
            .filter(d -> d.getDeletedAt() == null)
            .map(Demo::toDemoView).orElseThrow();
    result.setDemoId(query.getDemoId());
    Utils.logMethodFlow(this, "query", query, "END");
    return Single.of(result);
}
```

The provided code example showcases two `@QueryHandler` methods within a `DemoProjection` class:

* Both methods handle queries related to `DemoView`:
  * `query(DemoViewFindByIdQuery, ...)` handles finding a `DemoView` by its ID.
  * `query(DemoViewFindAllQuery)` handles retrieving all `DemoView` objects.
* The methods retrieve data from the `DemoRepository` based on the query type, filter out deleted entries, transform the data to `DemoView` objects, and construct the appropriate response (`Single` or `Multiple`).

#### Key Takeaways

* `@QueryHandler` empowers you to define methods within projections that act as handlers for specific queries.
* These methods retrieve data from the projection state and transform it into a format suitable for the query response.
* Understanding `@QueryHandler` is crucial for building effective projections that efficiently handle queries within your CQRS application.

**Optional Parameters and Advanced Topics:**

While the core structure focuses on the query object and response, the additional optional parameters (`QueryMessage`, `QueryGateway`, `Metadata`, and `Instant`) provide flexibility for more advanced scenarios. These parameters are covered in detail in separate chapters focusing on federated queries, metadata handling, and timestamping within Evento.
