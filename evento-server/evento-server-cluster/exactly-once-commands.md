---
description: Idempotency keys, derived keys for consumers, the service outcome store and caller deadlines
---

# Exactly-once Commands

In a distributed system a command can time out, or its server can die, after it was applied. The caller then sees an **indeterminate** outcome (`RequestTimeoutException`, `BrokerChangedException`) and the only safe retry is one the system can recognise as the same command. Evento does this with **idempotency keys**, checked by the server on whichever node the retry lands.

## Idempotency keys

Send a command with a key you choose — typically a client-generated request id:

```java
// default timeout
CompletableFuture<OrderCreatedEvent> r =
    commandGateway.sendIdempotent(new CreateOrderCommand(orderId, items), requestId);

// with metadata and an explicit timeout
commandGateway.sendIdempotent(command, requestId, metadata, 10, TimeUnit.SECONDS);
```

The server stores the key with the event the command produced. A later command with the **same key** for the same command type and aggregate is answered with the stored event, before any lock or forward, on any server (`event=idempotent_replay`, metric `evento.server.commands.idempotent.replayed`). The handler does not run again.

* A key already used by a **different** command is refused with `IdempotencyKeyMismatchException` (metric `…idempotent.mismatched`), never answered with the other command's event.
* Concurrent duplicates run the handler once. A retry that stops waiting on another execution of its key gets `IdempotencyKeyInProgressException` (indeterminate: retry again later).
* Only successes are recorded: a command refused by its handler can be retried with the same key.
* Keys starting with `evento:` are reserved and refused.
* The existing `send(...)` signatures are unchanged; a command sent without a key behaves as before.
* Keys cost no extra round trips: a keyed aggregate command runs the same two event-store statements as an unkeyed one.

{% hint style="info" %}
**What a caller should do.** On `RequestTimeoutException` or `BrokerChangedException`, retry the command with the **same** key. On `RequestNotSentException` (nothing was sent) any retry is safe. Never retry a non-idempotent command without a key: that is how the same effect gets applied twice.
{% endhint %}

## Keys derived for sagas, projectors and observers

Commands sent from a **saga, projector or observer** handler without a key get one automatically:

```
evento:<consumerId>:<event sequence number>:<CommandSimpleName>:<n>
```

where `n` counts the commands of that type in the handler invocation. A redelivered event, or a retried handler, re-issues the same keys, so the commands it sends are not executed twice — with no code change.

{% hint style="warning" %}
Keys never expire yet. A consequence: **rewinding a consumer** answers the commands it re-sends as replays of the stored events. To really run them again, rewind under a new consumer id (for example by bumping the component version).
{% endhint %}

## Service commands: the outcome store

For aggregate commands the server's record is enough. A **service** command has a window the server cannot close alone: the handler ran (with its side effects), but its event could not be stored — the append failed, or the server died between the handler's answer and the append. The server's retry would run the handler again.

The service bundle closes it by keeping its own record of each keyed execution:

```java
EventoBundle.Builder.builder()
    .setServiceCommandOutcomeStore(
        new JdbcServiceCommandOutcomeStore(appDataSource, SqlDialect.POSTGRES))   // or MYSQL
    // ...
```

A keyed service command whose key has a recorded outcome is answered with it and the handler is not run (`event=service_outcome_replayed`). `JdbcServiceCommandOutcomeStore` (module `evento-consumer-state-store-jdbc`) creates its table `evento_v2_service_outcome` with its own Flyway migration. `InMemoryServiceCommandOutcomeStore` exists for tests.

**The store must be shared by every instance of the service** that can receive the retry.

### Recording in the handler's transaction

Recording after the handler returns leaves one last gap: the process dying between the side effects and the record. When the side effects are writes to a database, record **in the same transaction**: inject `ServiceCommandOutcomes` into the `@CommandHandler`.

```java
@CommandHandler
PaymentDoneEvent handle(PayCommand cmd, ServiceCommandOutcomes outcomes) throws Exception {
    try (var con = dataSource.getConnection()) {
        con.setAutoCommit(false);
        try {
            insertPayment(con, cmd);
            var event = new PaymentDoneEvent(cmd.getOrderId());
            outcomes.recordWith(con, event);   // no-op without a key or a JDBC store
            con.commit();
            return event;
        } catch (Exception e) {
            con.rollback();                    // a DuplicateServiceOutcomeException too
            throw e;
        }
    }
}
```

The payment row and the outcome commit together or not at all. Two executions racing on one key collide on the outcome's primary key: the second gets `DuplicateServiceOutcomeException`, rolls back, and is answered with the first one's outcome. From a `MessageHandlerInterceptor` use `ServiceCommandOutcomes.current()`.

Side effects **outside** that database (a payment provider, an e-mail) are not covered by any store: pass the key downstream with `outcomes.idempotencyKey()` so the external system can deduplicate.

## Caller deadlines

Every request carries the caller's remaining time budget. The server turns it into a local deadline and **drops a command unexecuted** when the deadline has passed while it was queued, waiting for the aggregate lock, before the forward, or before the append (an aggregate handler that answered too late). Each drop logs `event=request_expired_dropped stage=…` and counts in `evento.server.requests.expired{stage}`.

Before, under load every timed-out command was still stored, and a saga retrying a "failed" payment could apply it several times. The caller normally does not see the drop — its own timer has already fired with `RequestTimeoutException` — but nothing runs for a caller that gave up. Do not branch on `RequestExpiredException`.

A service command is dropped only before its lock and its forward: once its handler has run, its event is always stored. A command that passes the last check and outlives its deadline during the append is still indeterminate — which is exactly what idempotency keys are for.

## Requirements

Keys are enforced on PostgreSQL with the full 2.5 schema (the `es__events.idempotency_key` column and its partial unique index, added online on the first boot). Otherwise — or during a rolling upgrade, on a 2.4 server — keyed commands run unkeyed with a warning. Upgrade all servers together.
