# EventoBundle

**EventoBundle** is a core class responsible for managing the lifecycle of an Evento Framework application. It handles the instantiation of components, consumer state stores, and connectivity with the cluster, providing a layer of abstraction for developers.

**Key functionalities:**

* **Component Management:** EventoBundle manages the discovery and instantiation of various application components like aggregates, services, projections, projectors, observers, and sagas. It uses reflection to scan the base package specified during configuration and identifies components based on annotations.
* **Consumer State Stores:** It facilitates the creation and management of consumer state stores. Consumer state stores track the processing state of event consumers, ensuring they don't miss or duplicate events.
* **Cluster Connectivity:** EventoBundle establishes and maintains the connection between the application and the Evento server cluster. It facilitates message exchange and coordinates consumer activities within the cluster.

**Starting an EventoBundle:**

To start an Evento Framework application, you use the `Builder` class provided by EventoBundle. This builder helps you configure various aspects of your application and eventually calls the `start()` method to initiate the application.

**Required Parameters for Builder:**

* `setBasePackage(package)`: Specifies the base package where EventoBundle should scan for components using reflection. This package should contain all your application classes with relevant annotations.
* `setBundleId(String)`: Assigns a unique identifier to your application.
* `setBundleVersion(long)`: Defines the version of your application. This is useful for managing deployments and rollouts.
* `setEventoServerMessageBusConfiguration(EventoServerMessageBusConfiguration)`: Provides configuration details for connecting to the Evento server cluster. This includes the cluster node address, retry attempts, and delay settings.

**Example Usage:**

```java
@Configuration
public class EventoConfiguration {

  @Bean
  @Scope(value = ConfigurableBeanFactory.SCOPE_SINGLETON)
  public EventoBundle eventoApplication(
      @Value("${evento.server.host}") String eventoServerHost,
      @Value("${evento.server.port}") Integer eventoServerPort,
      @Value("${evento.bundle.id}") String bundleId,
      @Value("${evento.bundle.version}") long bundleVersion
  ) throws Exception {
    return EventoBundle.Builder.builder()
        .setBasePackage(DemoWebApplication.class.getPackage())
        .setBundleId(bundleId)
        .setBundleVersion(bundleVersion)
        .setEventoServerMessageBusConfiguration(new EventoServerMessageBusConfiguration(
            new ClusterNodeAddress(eventoServerHost, eventoServerPort)
        )
            .setDisableDelayMillis(1000)
            .setMaxDisableAttempts(3)
            .setMaxReconnectAttempts(30)
            .setReconnectDelayMillis(5000)
        )
        .start();
  }
}
```

In this example, the `eventoApplication` bean leverages the `Builder` to configure the EventoBundle. It sets the base package, bundle ID, version, and configures the message bus using `EventoServerMessageBusConfiguration`. Finally, it calls the `start()` method to initiate the application.

**Additional Notes:**

* EventoBundle offers several optional configuration options through the `Builder` class, allowing you to customize aspects like performance services, query and command gateways, and autoscaling protocols.
* The chapter mentions additional functionalities like starting projector and saga event consumers. These functionalities are likely covered in separate sections as they involve managing specific consumer types.

I hope this comprehensive explanation clarifies the role and functionalities of EventoBundle in Evento Framework applications.
