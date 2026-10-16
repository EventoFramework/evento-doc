---
description: Run a bundle in a Spring Boot application from properties
---

# Spring Boot Starter

Since Evento **2.6**, `evento-spring-boot-starter` builds, starts and stops the bundle of a Spring Boot application from `evento.bundle.*` properties. It works with Spring Boot **3.x and 4.x** (it uses only the API they share and brings no Spring dependency of its own) and is Apache-2.0 like the other client libraries. Evento itself does not depend on Spring: the starter is optional, and an application can keep building `EventoBundle` by hand (see [Injector and @Component](injector-and-component.md)).

## Dependency

```gradle
implementation 'com.eventoframework:evento-spring-boot-starter:2.6.0'
```

```xml
<dependency>
    <groupId>com.eventoframework</groupId>
    <artifactId>evento-spring-boot-starter</artifactId>
    <version>2.6.0</version>
</dependency>
```

## Configuration

Only `evento.bundle.id` is required; without it the starter configures nothing.

```properties
evento.bundle.id=orders
evento.bundle.version=3
# host:port, the first is the preferred server, the others are fail-over targets
evento.bundle.servers=evento-eu-1:3030,evento-eu-2:3030
evento.bundle.auth-token=${EVENTO_BUNDLE_AUTH_TOKEN}
```

| Property | Default | Meaning |
|---|---|---|
| `evento.bundle.id` | — | The bundle id. Required. |
| `evento.bundle.instance-id` | random UUID | This instance's id. |
| `evento.bundle.version` | `1` | The bundle version. |
| `evento.bundle.base-package` | the `@SpringBootApplication` package | Where Evento components are scanned (sub-packages included). |
| `evento.bundle.description` | the id | What the console shows. |
| `evento.bundle.servers` | `localhost:3030` | Server addresses; the first is preferred (fail-back returns to it). |
| `evento.bundle.auth-token` | — | The server's `evento.server.bus.auth-token`. |
| `evento.bundle.expected-cluster-name` | — | Refuse servers announcing another `evento.cluster.name`. |
| `evento.bundle.zone` | — | Zone for `locality-preferred` routing. |
| `evento.bundle.default-request-timeout` | `30s` | Timeout of gateway calls without one. |
| `evento.bundle.tls.enabled` | `false` | Connect with TLS. |
| `evento.bundle.tls.trust-certs` | JDK trust store | PEM file with the CAs that sign the server's certificate. |
| `evento.bundle.tls.cert-chain`, `.private-key`, `.private-key-password` | — | This bundle's certificate and PKCS#8 key, for mutual TLS. |
| `evento.bundle.serialization.restrict` | `false` | Accept only the base package and `allowed-packages` as payload types (see [Security](../../evento-server/setup-evento-server/security.md)). |
| `evento.bundle.serialization.allowed-packages` | — | More payload packages, e.g. a shared API module. |
| `evento.bundle.consumer-state.store` | `auto` | `auto`: JDBC when `evento-consumer-state-store-jdbc` and a `DataSource` are present, else memory; `memory`; `jdbc`. |
| `evento.bundle.consumer-state.dialect` | `postgres` | `postgres` or `mysql`. |
| `evento.bundle.tracing.enabled` | `true` | Trace with the application's `OpenTelemetry` bean when `evento-opentelemetry` is present. |
| `evento.bundle.tracing.link-consumers` | `false` | Consumers start a new trace linked to the producer. |
| `evento.bundle.connection-readiness` | `false` | Readiness follows the connection to the server. |
| `evento.bundle.metrics-refresh` | `15s` | How often newly measured payload types get their meters. |
| `evento.bundle.auto-startup` | `true` | Start with the context. |
| `evento.bundle.shutdown-timeout` | `30s` | How long a graceful stop waits for the consumers. |

## What you get

* **The bundle runs with the context.** It starts once every bean exists, so components receive their constructor arguments from the context (repositories, clients), and stops gracefully before those beans go away: it leaves the server's routing, stops the consumers, closes the connection.
* **`CommandGateway` and `QueryGateway` beans**, injectable anywhere. A call before the bundle runs fails with a clear `IllegalStateException`.

```java
@RestController
class OrderController {
    private final CommandGateway commands;

    OrderController(CommandGateway commands) {
        this.commands = commands;
    }

    @PostMapping("/orders/{id}")
    CompletableFuture<?> create(@PathVariable String id) {
        return commands.send(new CreateOrderCommand(id));
    }
}
```

* **`EventoBundleStartedEvent`**, published when the server starts routing to the bundle, which can be after the context started: projectors with `waitForHeadReached` delay it until they catch up.
* **Metrics**, when Micrometer and a `MeterRegistry` are present: `evento.bundle.connected` (1 while connected), `evento.bundle.request{payload}` (round trip of the requests the bundle sends, with `.p99` and `.max`), `evento.bundle.handler{type}` (time its handlers run), all tagged `bundle` and `instance`.
* **Readiness**, with `evento.bundle.connection-readiness=true`: the application reports `REFUSING_TRAFFIC` while the bundle reconnects and `ACCEPTING_TRAFFIC` when it is back. It is off by default, as Spring Boot advises against readiness depending on an external system; turn it on when the application can serve nothing without Evento.

## Customizing the builder

Anything the properties do not cover goes into an `EventoBundleCustomizer` bean, which receives the `EventoBundle.Builder` before the bundle starts. Customizers run in `@Order`, after the starter's own, so they can override what the starter set.

```java
@Bean
EventoBundleCustomizer evento() {
    return builder -> builder
            .addConsumerExecutor(ConsumerExecutors.virtual("read-model", 64))
            .addUpcasters(OrderUpcasters.all());
}
```
