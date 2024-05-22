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

Advanced Configuration Options:

* `autoscalingProtocolBuilder` (Optional): This property allows you to specify a custom function for building the autoscaling protocol used by the bundle. Autoscaling helps your application dynamically adjust resource allocation based on workload demands. By default, a `SimpleAutoscalingProtocol` implementation is used that doesn't perform any specific actions on arrival or departure of the bundle instance.
* `consumerStateStoreBuilder` (Optional - Defaults to `InMemoryConsumerStateStore::new`): This property allows you to define a custom function for building the consumer state store. This store manages the state of event consumers within your bundle. By default, an in-memory consumer state store is used.
* `commandGatewayBuilder` (Optional - Defaults to `CommandGatewayImpl::new`): This property allows you to customize the creation of the command gateway within the bundle. The command gateway is responsible for routing commands to the appropriate component handlers. By default, a `CommandGatewayImpl` is used.
* `queryGatewayBuilder` (Optional - Defaults to `QueryGatewayImpl::new`): Similar to `commandGatewayBuilder`, this property allows you to customize the creation of the query gateway within the bundle. The query gateway is responsible for routing queries to the appropriate component handlers. By default, a `QueryGatewayImpl` is used.
* `performanceServiceBuilder` (Optional - Defaults to `RemotePerformanceService(eventoServer, 1)`): This property allows you to define a custom function for building the performance service within the bundle. This service monitors and reports on the performance of the bundle. By default, a `RemotePerformanceService` is used, which sends performance data to the Evento server.
* `sssFetchSize` (Optional - Defaults to 1000): This property defines the number of events retrieved from the consumer state store in a single fetch operation. Adjusting this value can influence performance and resource utilization.
* `sssFetchDelay` (Optional - Defaults to 1000): This property defines the delay (in milliseconds) between subsequent fetches from the consumer state store. This value can be used to optimize event processing based on workload characteristics.
* `tracingAgent` (Optional - Defaults to a new `TracingAgent` instance with bundleId and bundleVersion): This property allows you to set a custom tracing agent for the bundle. Tracing agents help track the execution flow of events and commands within your application. By default, a new `TracingAgent` instance is created with the bundle's ID and version.
* `injector` (Optional - Defaults to a function returning null): This property allows you to define a custom function for injecting dependencies into your components. This advanced option provides flexibility for configuring specific injection behavior for your bundle.

**Additional Notes:**

* EventoBundle offers several optional configuration options through the `Builder` class, allowing you to customize aspects like performance services, query and command gateways, and autoscaling protocols.
* The chapter mentions additional functionalities like starting projector and saga event consumers. These functionalities are likely covered in separate sections as they involve managing specific consumer types.

I hope this comprehensive explanation clarifies the role and functionalities of EventoBundle in Evento Framework applications.
