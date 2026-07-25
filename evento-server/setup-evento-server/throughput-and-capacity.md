---
description: How many concurrent requests a server can absorb, and what happens past that
---

# Throughput and Capacity

Every request a bundle sends carries a deadline. The gateway default is 30 seconds, after which the caller stops waiting and the correlation entry is dropped. That single fact is what makes capacity planning on the bus different from capacity planning on a plain HTTP service: work that arrives faster than the server can serve it does not simply take longer, it eventually stops counting at all, because the client it belonged to has already gone.

## The capacity of one server

Three limits sit in series between an inbound frame and a response. A request is bounded by the smallest of them.

| Limit | Property | Default |
| --- | --- | --- |
| Threads handling bundle requests | `evento.server.bus.business-executor-max-size` | `cores × 8` |
| Requests waiting for one of those threads | `evento.server.bus.business-executor-queue-capacity` | `256` |
| Concurrent event-store fetches | `evento.es.fetch.concurrency` | `4` |

The first is the one operators reach for. The third is the one that usually binds first on a consumer-heavy cluster: `EventFetchRequest` is served by the broker itself under a fair semaphore, so no matter how many bus threads exist, only four event fetches run at once. Each fetch transiently holds a full result set, its deserialised event graph and the encoded response on heap, which is why the limit exists — raise it against measured heap headroom, not hopefully.

A useful first estimate of steady-state capacity:

```
sustainable requests/second ≈ business-executor-max-size ÷ mean service time (seconds)
```

Sixty-four threads serving 20 ms requests is roughly 3,200 requests/second. If the arrival rate stays under that, the queue stays near empty and latency is just service time. If it goes over, the queue absorbs the difference — briefly.

## What exceeding it looks like

The failure is not gradual. Suppose 64 threads, a 256-deep queue, 20 ms of service time and the default 30-second client deadline. A full queue represents 256 × 20 ms ÷ 64 ≈ 80 ms of backlog, which is harmless. Now let service time rise to 500 ms because the database got slower: the same queue is 2 seconds deep, and arrivals keep coming. The queue fills, the pool is already at maximum, and the server begins running tasks on the Netty event loop — which stops it reading from sockets and pushes back on clients through TCP. That is the design working.

What turns this into a collapse is the deadline. Once queue wait plus service time exceeds 30 seconds, every request that comes out of the queue belongs to a caller that has stopped waiting. The server is fully busy producing responses nobody will read, so effective throughput approaches zero while CPU looks unremarkable and both databases look idle. Clients see timeouts, retry, and add more arrivals to a system already past capacity.

{% hint style="danger" %}
Congestion collapse is self-sustaining. It does not recover when the load that triggered it stops, because retries keep the arrival rate high. Reducing client concurrency is what breaks the cycle — and counter-intuitively, fewer concurrent clients can yield **more** completed work, because requests finish inside their deadline instead of expiring in a queue.
{% endhint %}

A real instance of this: a bulk catalogue import running 20 concurrent writers against an 8-core server degraded from 16 writes/second to 0.07/second, with 250 command timeouts per hour. Dropping the client to 8 concurrent writers — below the server's thread count — restored 25 writes/second with no timeouts at all. The server had never been short of CPU, memory or database connections.

{% hint style="warning" %}
A queue deeper than deadline ÷ service time is dead work by construction: anything behind that point expires before it is served. This is why the queue default is small. Enlarging it to "handle more load" makes the collapse worse, not better — it buys queueing delay with the client's deadline.
{% endhint %}

## Detecting it

The bus executor publishes its own state through Micrometer, on `/actuator/prometheus`:

* `evento.server.bus.executor.pool.size` and `…max` — how much of the configured capacity is actually in use.
* `evento.server.bus.executor.queue.depth` — requests waiting for a thread. Sustained non-zero depth is the early warning, arriving well before anything fails.
* `evento.server.bus.executor.saturated` — a counter incremented only when the pool is at maximum **and** the queue is full, so the caller had to run the task itself. **This is the meter to alert on.** Any sustained increase means arrivals exceed everything this server can do.

Two log lines say the same thing without a metrics stack. The server logs saturation directly:

```
event=bus_business_executor_saturated total=412 poolSize=64 max=64 queueDepth=256 submitted=320
```

and both sides log expiries, the bundle broken down by message type so you can see *what* is drowning:

```
event=correlations_expired count=5 pending=5
event=bundle_correlation_expired count=12 pending=48 byType={CatalogProductAddCommand=12}
```

Expiries are logged at `WARN`. Treat a steady stream of them as capacity exhaustion rather than as unlucky individual requests.

## Reacting to it

**Raise capacity** when the host has headroom: increase `business-executor-max-size`, and `evento.es.fetch.concurrency` if the expiring payload type is `EventFetchRequest`. Check that downstream capacity grows with it — a bundle's connection pool must be able to satisfy the extra concurrent handlers, or you have only moved the queue.

**Reduce demand** when it does not. Client concurrency is the fastest lever and the only one that works during an active collapse. Since 2.4.0 a bundle can also bound itself: `BundleClientConfig.Builder.maxInFlightRequests(n)` refuses a request outright with `TooManyPendingRequestsException` once `n` are already outstanding. That failure is immediate and definite — nothing was sent, so it is always safe to retry after backing off — which is strictly better for a caller than spending a full 30-second deadline to fail anyway.

**Scale out** when one server is genuinely the limit; see [Evento Server Cluster](../evento-server-cluster.md). Partitioning by [context](../../evento-framework/eventobundle/context.md) spreads consumers across servers, and for write-side throughput the choice of component matters as much as any pool size — see [Choosing a Write Strategy](../../evento-framework/component/choosing-a-write-strategy.md), since aggregates serialise per context while services do not.

## A note on timeouts and retries

When a request expires, the caller gives up but **nothing cancels the work**. The handler may still be running, and may complete successfully long after the caller has been told it failed.

Since 2.4.0 that outcome is typed: an expiry surfaces as `RequestTimeoutException` rather than a generic failure, so an application can distinguish "we do not know" from a handler that definitely rejected the message. Report it as indeterminate — HTTP 504 rather than 500 — and retry only idempotent work or work carrying a deduplication key. Retrying a non-idempotent command after a timeout is how the same effect gets applied twice.

{% hint style="info" %}
This is the request path. Consumers have their own capacity story — bounded executors, permits and saturation counters — described in [Parallel Consumers](../../evento-framework/eventobundle/parallel-consumers.md). The vocabulary is deliberately the same: capacity, in flight, saturated.
{% endhint %}
