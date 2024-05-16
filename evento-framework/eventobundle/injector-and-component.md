---
description: Simplifying Component Management
---

# Injector and @Component

In the realm of complex applications built with modular components, managing dependencies between them can quickly become a tangled mess. This is where Dependency Injection (DI) shines, promoting loose coupling and fostering code maintainability. The Evento framework embraces DI principles, offering a streamlined approach to handling component lifecycles and dependency resolution.

#### Introducing the Injector: The Dependency Resolver

The `Injector` interface serves as the heart of Evento's DI system. It acts as a powerful function that takes a class as input and returns a corresponding instance. This instance will have all its required dependencies fulfilled through the injector's magic.

**Behind the Scenes:**

* When Evento encounters a class marked with `@Component` or its derivatives, the framework utilizes the configured injector to create an instance. This instance is managed internally by Evento and is not directly exposed for injection into other components.
* The injector examines the component's constructor, identifying any dependencies declared as parameters.
* The injector then recursively retrieves these dependencies using itself, ensuring a chain reaction of dependency resolution.

**Spring Integration Example:**

The provided code snippet showcases how Evento integrates with Spring Boot's dependency injection:

```java
@Projector(version = 3)
public class DemoProjector {

  private final DemoRepository demoRepository;

  public DemoProjector(DemoRepository demoRepository) {
    this.demoRepository = demoRepository;
  }

  // ...
}
```

In this example, `DemoProjector` is a component requiring a `DemoRepository` instance. During bundle creation:

```java
EventoBundle.Builder.builder()
  .setBasePackage(DemoQueryApplication.class.getPackage())
  .setConsumerStateStoreBuilder(InMemoryConsumerStateStore::new)
  .setInjector(factory::getBean) // Spring's getBean function as injector
  .setBundleId(bundleId)
  // 
```

We configure the `setInjector` method with `factory::getBean`. This essentially tells Evento to leverage Spring's `getBean` function to resolve dependencies for the components Evento manages internally. When `DemoProjector` is instantiated, the injector (Spring's `getBean` in this case) will locate and provide the required `DemoRepository` instance.

**Benefits of Evento's DI:**

* **Simplified Component Management:** Evento handles component lifecycles, reducing boilerplate code.
* **Improved Code Maintainability:** Loose coupling through constructor injection promotes testability and modularity.
* **Flexibility:** Supports various injector implementations for integration with different frameworks.

**In Conclusion:**

Evento's DI approach, with its `@Component` annotations and the powerful `Injector` interface, streamlines the process of creating and managing internal components. By leveraging existing frameworks like Spring, Evento simplifies dependency resolution within your application. Remember, the chosen injector depends on your framework or custom implementation.
