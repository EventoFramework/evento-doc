# @Invoker

The RECQ architecture emphasizes modularity and separation of concerns. In this context, the `@Invoker` annotation plays a crucial role in defining classes that act as orchestrators, bridging the gap between the external world and the internal components.

#### Understanding `@Invoker`

The `@Invoker` annotation marks a class within your Evento application as an invoker. Invokers are responsible for initiating operations or invoking methods on other components within the system. They serve as a facade, offering a simplified interface for external interactions.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Component
public @interface Invoker {
}
```

Here's a breakdown of the annotation's definition:

* **`@Retention(RetentionPolicy.RUNTIME)`:** Ensures the annotation information is retained at runtime, allowing Evento to identify invoker classes.
* **`@Target(ElementType.TYPE)`:** Specifies that the annotation can only be applied to class declarations.
* **`@Component`:** Inherits from the `@Component` annotation, indicating that the annotated class is a component within the Evento framework.

#### Invokers and the RECQ Component Pattern

The RECQ pattern promotes well-defined component types. Invokers act as a bridge between the external API layer and the internal domain logic or services. They shield the complexities of the underlying architecture from external consumers.

Here are some key characteristics of invokers:

* **Abstraction:** They provide a simplified interface for interacting with the system, often using plain Java methods (similar to a REST API).
* **Orchestration:** They might orchestrate calls to multiple services, projections, or sagas to fulfill a specific request.
* **Command/Query Gateway Access:** Invokers typically leverage the `CommandGateway` to send commands and the `QueryGateway` to execute queries within the system.

#### The `InvokerWrapper` Class

```java
/**
 * The InvokerWrapper class is an abstract class that serves as a wrapper for the command and query gateways.
 * It provides methods to retrieve the command and query gateways.
 */
public abstract class InvokerWrapper {

    /**
     * Retrieves the command gateway.
     *
     * @return the command gateway
     * @throws RuntimeException if the command gateway is unavailable.
     */
    protected CommandGateway getCommandGateway() {
       throw new RuntimeException("getCommandGateway() called outside an @InvocationHandler scope.");
    }

    /**
     * Retrieves the query gateway.
     *
     * @return the query gateway
     * @throws RuntimeException if the query gateway is unavailable.
     */
    protected QueryGateway getQueryGateway() {
       throw new RuntimeException("getQueryGateway() called outside an @InvocationHandler scope.");
    }

}
```

The provided code snippet showcases the `InvokerWrapper` class, an abstract class often used in conjunction with `@Invoker`. This class serves two primary purposes:

1. **Command/Query Gateway Access Restriction:** It defines abstract methods for retrieving the `CommandGateway` and `QueryGateway`. In concrete invoker implementations, these methods are usually overridden to provide access only within `@InvocationHandler` methods (discussed later). This ensures proper usage of the gateways within the context of handling incoming requests.
2. **Template for Gateway Access:** Concrete invoker implementations can extend `InvokerWrapper` and provide specific logic for retrieving the gateways within their `@InvocationHandler` methods.

#### Invoker in Action: The `DemoInvoker` Example

```java
@Invoker
public class DemoInvoker extends InvokerWrapper {


    @InvocationHandler
    @Track
    public CompletableFuture<Collection<DemoView>> findAll(@RequestParam int page) {
       Utils.logMethodFlow(this, "findAll", page, "BEGIN");
       var resp = getQueryGateway()
             .query(new DemoViewFindAllQuery(10, page * 10))
             .thenApply(Multiple::getData);
       Utils.logMethodFlow(this, "findAll", page, "END");
       return resp;
    }


    @InvocationHandler
    @Track
    public CompletableFuture<DemoView> findById(@PathVariable String identifier) {
       Utils.logMethodFlow(this, "findById", identifier, "BEGIN");
       var resp = getQueryGateway().query(new DemoViewFindByIdQuery(identifier)).thenApply(Single::getData);
       Utils.logMethodFlow(this, "findById", identifier, "END");
       return resp;
    }


    @InvocationHandler
    @Track
    public CompletableFuture<?> save(@RequestBody DemoPayload demoPayload) {
       Utils.logMethodFlow(this, "save", demoPayload, "BEGIN");
       return getCommandGateway().send(new DemoCreateCommand(
             demoPayload.getDemoId(), demoPayload.getName(), demoPayload.getValue()
       )).whenComplete((a,b) -> Utils.logMethodFlow(this, "save", demoPayload, "END"));
    }


    @InvocationHandler
    @Track
    public CompletableFuture<?> update(@RequestBody DemoPayload demoPayload, @PathVariable String identifier) {
       Utils.logMethodFlow(this, "update", demoPayload, "BEGIN");
       demoPayload.setDemoId(identifier);
       return getCommandGateway().send(new DemoUpdateCommand(
             demoPayload.getDemoId(), demoPayload.getName(), demoPayload.getValue()
       )).thenApply(o -> {
          Utils.logMethodFlow(this, "update", demoPayload, "END");
          return o;
       });
    }


    @InvocationHandler
    @Track
    public CompletableFuture<?> delete(@PathVariable String identifier) {
       Utils.logMethodFlow(this, "delete", identifier, "BEGIN");
       return getCommandGateway().send(new DemoDeleteCommand(identifier
       )).thenApply(o -> {
          Utils.logMethodFlow(this, "delete", identifier, "END");
          return o;
       });
    }

}
```

The provided `DemoInvoker` class demonstrates how `@Invoker` is used:

* It extends `InvokerWrapper`.
* It defines several methods annotated with `@InvocationHandler` and `@Track` (tracking might be for logging or monitoring purposes).
* Each method represents an operation exposed by the invoker:
  * `findAll` and `findById` use the `QueryGateway` to retrieve data through queries.
  * `save`, `update`, and `delete` use the `CommandGateway` to send commands for creating, updating, and deleting data.
* These methods delegate the actual work (fetching data or sending commands) to the respective gateways, providing a higher-level abstraction for external interaction.

#### Key Takeaways

* `the @Invoker` helps define classes that act as entry points for interacting with the RECQ architecture.
* Invokers provide a simplified interface, often mimicking a REST API, for external systems to interact with the application.
* They leverage `CommandGateway` and `QueryGateway` to orchestrate operations within the system.
* The `InvokerWrapper` class provides a foundation for implementing invokers with restricted gateway access and potential gateway retrieval logic.

By understanding `@Invoker`, you can effectively design facades that simplify interactions with your Evento applications, adhering to the principles of the RECQ architecture.
