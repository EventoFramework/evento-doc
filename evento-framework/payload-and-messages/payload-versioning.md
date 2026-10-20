---
description: Changing payload classes without losing the history written with their old shape
---

# Payload Versioning and Upcasting

An event store is append-only: an event written two years ago keeps the shape its class had two years ago. Evento stores a payload as JSON, `["com.acme.OrderPlaced", { …fields… }]`, and routes events by their simple class name, so as long as the class only gains or loses fields, Jackson absorbs the difference and nothing needs to be done. When a change goes further — a field renamed, split or changing meaning, a class renamed or moved — the old events can no longer be read into the new class.

Since Evento **3.0** payloads are **versioned**: a class declares its *revision*, every payload records the revision it was written with, and the bundle registers **upcasters** that turn an older shape into the next one *at read time*, before Jackson sees it. The history is never rewritten.

{% hint style="info" %}
This is the strategy of Axon Framework (`@Revision` + an upcaster chain applied while reading). The store is evidence of what happened: an upcaster that turns out wrong is fixed and applies to every later read, while a migrated store cannot be un-migrated.
{% endhint %}

## When do I need a revision?

| Change | Revision needed? |
|---|---|
| A field added (old events read it as `null`/default) | No |
| A field removed (old events carry it, it is ignored) | No |
| A field renamed, split, merged, or whose meaning or unit changed | **Yes** — raise the revision and register an upcaster |
| A class renamed or moved to another package | **Yes** — register a *rename* step (see below) |

## Declaring a revision

Annotate the payload class with `@Revision(n)`. A class without the annotation is revision `0`, and so is everything written before 3.0: existing stores need no migration.

```java
import com.evento.common.versioning.Revision;

/** Revision 0 called the title "name" and had no quantity. */
@Revision(1)
public class ItemAdded extends DomainEvent {
    private String itemId;
    private String title;
    private int quantity;
    // constructors, getters
}
```

`@Revision` works on every payload: domain and service events, commands, queries, and an aggregate's state (its snapshots). It is not inherited: each class declares its own.

## Writing upcasters

An `Upcaster` is one step of the chain: *payload X at revision N becomes …*. It receives the payload's fields as a Jackson `ObjectNode` and edits it in place.

**A revision step** — same class, the revision must rise:

```java
Upcaster.from(ItemAdded.class, 0).to(1, json -> {
    json.set("title", json.remove("name"));   // renamed field
    json.put("quantity", 1);                  // new field with the value old events implied
});
```

**A rename step** — the payload becomes another class. Name the old class by its *simple name*, so it can be deleted from the code base:

```java
// ItemRenamed was replaced by ItemRenamedV2; the old class no longer exists
Upcaster.from("ItemRenamed", 0).to(ItemRenamedV2.class, 0, json -> json.put("reason", "legacy"));

// a pure rename, no field changes
Upcaster.from("OrderPlaced", 0).to(OrderPlacedV2.class, 0);
```

Steps chain on their own: an `ItemAdded` at revision 0 goes through `0 → 1`, then `1 → 2` if you add that step later, and a renamed payload continues with the steps of its new class. Every handler only ever sees the **current** shape.

### Revision or a new "V2" class?

Both are supported, and the rename is just one more step of the chain. Prefer a **revision of the same class** for shape changes: a new class per change makes every consumer handle every version forever and leaks version numbers into routing names. Create a **new class** when the meaning of the message changes and the new name tells the reader something; then register a rename step, delete the old class, and only the new one has handlers.

## Registering the chain

Upcasters are registered on the bundle:

<pre class="language-java"><code class="lang-java">EventoBundle.Builder.builder()
...
<strong>.addUpcasters(
</strong><strong>        Upcaster.from(ItemAdded.class, 0).to(1, json -> json.set("title", json.remove("name"))),
</strong><strong>        Upcaster.from("ItemRenamed", 0).to(ItemRenamedV2.class, 0),
</strong><strong>        Upcaster.from(ItemState.class, 0).to(1, json -> json.set("title", json.remove("name"))))
</strong>...
</code></pre>

The chain is validated when the bundle starts, before it connects: two steps from the same payload and revision, a revision step that does not rise, or a loop of renames fail start-up. A good habit is one `Upcasters`/`Upcaster[]` constant per bounded context, the "history" of its payloads, shared by every bundle that reads them.

## Where upcasting runs

Upcasting happens in the bundle, where the classes are; the Evento Server stays payload-agnostic and stores bytes untouched. It is applied on every read path:

* events delivered to **projectors, sagas and observers**, including [dead event](../dead-event-queues.md) retries;
* the **event stream and the snapshot** an aggregate is rebuilt from (upcast the aggregate state class too, if it changed);
* **commands and queries** received by a handler.

A **renamed command or query** keeps being routed under its former name: the bundle declares its handler for the old name as well, so callers that still send `RenameItem` reach the handler of `RenameItemV2` until they are upgraded.

## When an upcaster fails

An upcaster that throws stops its consumer **at that event** (logged as `event=upcast_failed`, with the payload name and revision) and the consumer retries it, rather than dead-lettering every old event of that type. Fix the upcaster and redeploy: the consumer resumes from the same event.

## Upgrade order

{% hint style="warning" %}
**Upgrade the Evento Servers to 3.0 before deploying a class with `@Revision`.** An older server re-encodes payload envelopes without the revision, so a revised payload would be stored as revision 0 and upcast again on every read. A 3.0 bundle detects such a server (it lacks the `revision:1` capability) and refuses to send or store a revised payload through it, with an error that says so. Unrevised payloads, the default, flow through any server.
{% endhint %}

## Things to know

* Upcasters see the JSON as Evento stores it. Values whose declared type is not final (a `List`, a `Map`, a `BigDecimal`, a non-final class) carry their type next to them: a list appears as `["java.util.ArrayList", [ … ]]`, a decimal as `["java.math.BigDecimal", 1.10]`. Decimals keep their exact value through the chain.
* Not covered: **downcasting** for readers older than the writer (rely on the tolerant reader instead: unknown fields are ignored), **splitting** one event into several, upcasting **saga state** and **query answers (views)**, and changes to metadata.
