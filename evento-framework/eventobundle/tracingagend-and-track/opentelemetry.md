---
description: Follow a request across bundles and the server with OpenTelemetry
---

# OpenTelemetry

Since Evento **2.6**, `evento-opentelemetry` traces a bundle with [OpenTelemetry](https://opentelemetry.io/). It is opt-in: a bundle without it keeps the no-op `TracingAgent` and pays nothing.

```gradle
implementation 'com.eventoframework:evento-opentelemetry:2.6.0'
```

The module depends on the OpenTelemetry **API** only: your application provides the SDK (or runs the [OpenTelemetry Java agent](https://opentelemetry.io/docs/zero-code/java/agent/)) and decides where spans go.

```java
EventoBundle.Builder.builder()
        .setTracingAgent(new OpenTelemetryTracingAgent("orders", 1, GlobalOpenTelemetry.get()))
        // ...
        .start();
```

With the [Spring Boot Starter](../spring-boot-starter.md) there is nothing to write: an `OpenTelemetry` bean is used automatically.

## What is traced

* **A span per handler**, named `<component> <payload>` (for example `OrderAggregate CreateOrderCommand`): `SERVER` for commands, queries and invocations, `CONSUMER` for the events of projectors, sagas and observers. A handler that throws records the exception and an error status.
* **A span per command or query sent**, named `send <command>` or `query <query>` (`CLIENT`), from the send to the reply, with the error when the reply is a failure: it shows how long the caller waited, wire and server included.
* **The trace context travels in the message metadata** as W3C `traceparent` / `tracestate`: every command and query sent carries its send span, and the event a command produces carries the aggregate's span and is stored with it. A projector consuming that event later continues the same trace.
* **Application code joins too.** The gateways `EventoBundle.getCommandGateway()` / `getQueryGateway()` (and the starter's beans) start their send span under the current one, so a trace started by an HTTP request reaches the handlers.
* **The server** adds a span for each command it executes (`evento command <payload>`), with the time of each phase (`evento.phase.lock.ms`, `.story.ms`, `.append.ms`, …) as attributes, and the aggregate's span as its child. It uses the OpenTelemetry Java agent attached to the server, or nothing: without an agent the API is a no-op. `evento.server.tracing.enabled=false` turns it off.

```
POST /orders                                     (your HTTP span)
└── send CreateOrderCommand                      (bundle: until the reply)
    └── evento command CreateOrderCommand        (server: lock, story, append)
        └── OrderAggregate CreateOrderCommand    (bundle)
            └── OrderProjector OrderCreatedEvent (bundle, when the event is consumed)
```

## Consumers: child or link

By default a consumer span is a **child** of the span that produced the event, so one trace goes from the request to the read models. When events are consumed long after they were written (replays, a new projector catching up), that makes very long traces: `agent.linkingConsumers()` (starter: `evento.bundle.tracing.link-consumers=true`) starts a new trace for each consumed event, **linked** to the producer.

{% hint style="info" %}
Queries and other requests the server only forwards are not traced on the server: it carries their bytes without decoding them. The send span and the handler span still belong to the same trace. Stream queries (`QueryGateway.stream`) have no single reply, so they get no send span: the handler span joins the caller's trace directly.
{% endhint %}
