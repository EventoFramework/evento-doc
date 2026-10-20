---
description: Given/when/then tests of aggregates, sagas, projectors and services
---

# Testing with Fixtures

Evento handlers are plain methods: an aggregate decides an event from its state and a command, a saga reacts to an event with commands. Since Evento **2.6**, `evento-test` runs a component's own handlers the way a bundle does, with no server, no event store and no database.

```gradle
testImplementation 'com.eventoframework:evento-test:2.6.0'
```

The fixtures do not depend on a test framework: an expectation that fails throws an `AssertionError`, and every result also exposes its raw values for AssertJ or Hamcrest.

## Aggregates

```java
AggregateFixture.of(new OrderAggregate())
        .given(new OrderCreatedEvent("o1", 100), new ItemAddedEvent("o1", "pen", 60))
        .when(new AddItemCommand("o1", "ink", 30))
        .expectEvent(new ItemAddedEvent("o1", "ink", 30))
        .expectState(OrderState.class, s -> assertEquals(90, s.getSpent()));
```

* `given(events...)` is the history; it goes through the `@EventSourcingHandler`s. `givenState(state)` starts from a snapshot. With neither, the command must be an initializer (`init = true`).
* `expectEvent(event)`, `expectEvent(Type.class, check)`, `expectException(Type.class[, check])`, `expectState(Type.class, check)`, `expectDeleted()`, `expectCommandsSent(...)`.
* The framework's own rules apply: an initializer on an existing aggregate fails with `AggregateInitializedError`, a command on a missing one with `AggregateNotInitializedError`.

## Sagas

```java
var fixture = SagaFixture.of(new PaymentSaga());
fixture.queryGateway().answer(FindPrice.class, q -> Single.of(new PriceView(10)));

fixture.given(new OrderCreatedEvent("o1"), new ItemAddedEvent("o1", "pen"))
        .whenEvent(new OrderPaidEvent("o1"))
        .expectCommands(new ChargeCommand("o1", 10))
        .expectEnded();
```

`expectCommands(...)` (exactly these, in order), `expectCommand(Type.class, check)`, `expectNoCommands()`, `expectEnded()`, `expectNotEnded()`, `expectAssociation(property, value)`, `expectState(...)`, `expectException(...)`.

## Projectors

The projector is built with its repository, real or in memory, and the test asserts on the repository.

```java
var orders = new InMemoryOrderRepository();
ProjectorFixture.of(new OrderProjector(orders))
        .given(new OrderCreatedEvent("o1"))
        .whenEvent(new OrderConfirmedEvent("o1"))
        .expectSuccess();
assertEquals("CONFIRMED", orders.find("o1").status());
```

Events arrive live (`ProjectorStatus.isHeadReached()` is true); `replaying()` makes the handlers see a replay.

## Services

```java
ServiceFixture.of(new PaymentService(fakeProvider))
        .when(new ChargeCommand("o1", 30))
        .expectEvent(new OrderChargedEvent("o1", 30));
```

`expectEvent(...)`, `expectNoEvent()`, `expectException(...)`, `expectCommandsSent(...)`.

## Gateways

Every fixture passes the handlers a `RecordingCommandGateway` (`commandGateway()`), which records the commands and answers with stubs (`answer(Type.class, command -> result)`, `null` by default), and a `StubQueryGateway` (`queryGateway()`), which answers from stubs and **fails a query that has none**, so a test never passes on an answer it did not mean. Both can also be passed to any class that takes a gateway.

## Equality

Payloads are compared with `equals` when it says they are equal, otherwise field by field, so payload classes do not need to implement `equals`. A mismatch prints both payloads.

{% hint style="warning" %}
Payload classes must be top-level classes. Evento routes payloads by the class name after the last dot, so a nested class (`Outer$Inner`) is not routed in a bundle, and the fixture fails the same way.
{% endhint %}

Retries, dead-event queues and checkpoints belong to the consumer engines and are not part of the fixtures: test them with a real bundle against a broker, as below.

## Integration tests with a broker

Two ways to run a real bundle in a test, from 2.6:

* **`EventoTestBroker`** (`com.eventoframework:evento-test-broker`, test scope): the server's own broker and aggregate command handling in the test's JVM, on a free port, with an in-memory event store. Aggregate commands are stored as events, projectors, sagas and observers read them, queries are routed. No database, no container, one broker per test. It runs server code, so the tests need Java 25.

```java
try (var broker = EventoTestBroker.start()) {
    var bundle = EventoBundle.Builder.builder()
            .setBasePackage(OrderAggregate.class.getPackage())
            .setBundleId("orders")
            .setEventoServerMessageBusConfiguration(broker.busConfiguration())
            .setConsumerEngineConfigBuilder(ConsumerEngineConfig::inMemory)
            .start();
    bundle.getCommandGateway().send(new CreateOrder("o-1")).get();
    assertThat(broker.events()).hasSize(1);
    broker.publish(new PaymentReceived("o-1"), "o-1"); // an event for the consumers
}
```

* **`EventoServerContainer`** (`evento-test`, with Testcontainers in the test's dependencies): the real server image, on a PostgreSQL the test starts. The full server (persistence, locks, web console API), out of process: it works with tests on Java 21 and any Spring Boot version.

```java
var network = Network.newNetwork();
var postgres = new PostgreSQLContainer<>("postgres:16").withNetwork(network).withNetworkAliases("pg");
var evento = new EventoServerContainer()   // ghcr.io/eventoframework/evento-server:<this version>
        .withNetwork(network)
        .withDatabase("jdbc:postgresql://pg:5432/" + postgres.getDatabaseName(),
                postgres.getUsername(), postgres.getPassword())
        .dependsOn(postgres);
evento.start();
// ... .setEventoServerMessageBusConfiguration(evento.busConfiguration())
```
