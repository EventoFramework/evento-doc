---
description: Rollout order and behaviour changes for 2.6 (query path and payload versioning)
---

# Upgrading to 2.6

2.6 changes the query path (streamed, paged and locally answered queries, read-your-writes, compression, bounded server memory) and adds [payload versioning](../../evento-framework/payload-and-messages/payload-versioning.md). There is **no database schema change**. Wire changes are additive and negotiated in the handshake (capabilities `stream:1` and `revision:1`): 2.5 and 2.6 bundles and servers interoperate in any mix, with the exceptions below.

## 1. Servers first, then the bundles

Upgrade the servers, then roll the bundles at your own pace. Servers can be upgraded one at a time.

{% hint style="warning" %}
**A class annotated with `@Revision` needs 2.6 servers.** A 2.5 server re-encodes payload envelopes without their revision, so a 2.6 bundle refuses to send or store a revised payload through it (the error says so). Deploy the first `@Revision` only once every server is on 2.6. Unrevised payloads, the default, flow through any server.
{% endhint %}

## 2. Queries are "straight"

A 2.6 server routes a query declared by a 2.6 handler bundle straight: its answer is not kept for exactly-once replays and not buffered while the caller reconnects (queries are idempotent reads; keeping answers is what filled the server's heap with large results). A 2.6 caller that loses its session while a query is in flight **asks it again** on its next session, on whatever server. A 2.5 caller in the same situation now waits for its timeout instead of getting the buffered answer: **upgrade callers along with the handler bundles**.

Event fetches of the consumers are asked again after a lost session in the same way.

## 3. Review the server's memory bounds

What the server keeps for commands is now bounded in bytes as well as in entries. The defaults fit most deployments; see `evento.server.bus.dedup.*`, `evento.server.bus.reconnect-buffer.max-bytes` and `evento.server.bus.compression.threshold-bytes` in [Advanced Options](../setup-evento-server/advanced-options.md).

## 4. Adopt the new features where they pay off

Nothing has to change in the bundles' code. Then, where useful:

* `QueryGateway.stream(...)`, `Streamed<View>`, `Page<View>` and direct streams for large answers: [Streamed and Paged Queries](../../evento-framework/component/projection/streaming-and-paged-queries.md).
* `CommandGateway.sendTracked(...)` and `QueryOptions.after(token)` / `readYourWrites()`: [Read Your Writes](../../evento-framework/component/projection/read-your-writes.md).
* `@Revision` and upcasters when a payload class must change shape or name: [Payload Versioning and Upcasting](../../evento-framework/payload-and-messages/payload-versioning.md).

A bundle now answers the queries it handles itself, without the server (`setLocalQueryShortCircuit(false)` to turn it off). Tracing, metrics and the GUI see these queries as before.

Code that asserts the exact capability set of a bundle's handshake must expect `stream:1` and `revision:1`.
