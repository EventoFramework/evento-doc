---
description: Keep personal data in an immutable event store and still honour the right to erasure
---

# Personal Data and the Right to Erasure

Events are never changed or deleted, and the GDPR (and similar laws) gives people the right to have their personal data erased. Evento reconciles the two with **crypto-shredding**: personal data is stored encrypted with a key of its own person, the *data subject*, and erasing it means deleting that key. The events stay, with everything that is not personal; what was personal can no longer be read by anyone, in the event store, in snapshots, or in backups.

## Marking personal data

Mark the fields with `@PersonalData`, and the field that says whose they are with `@DataSubject`:

```java
public class CustomerRegistered extends DomainEvent {
    @DataSubject String customerId;
    @PersonalData String name;
    @PersonalData String email;
    @PersonalData Address address;
    int loyaltyPoints;
    // constructors, getters
}
```

That is all. When the bundle writes the payload, each `@PersonalData` field becomes an encrypted string (AES-256-GCM, with the key of `customerId`); when it reads it, the field is decrypted. Handlers, aggregates, projectors and sagas see plain values. The same works in commands, aggregate states (snapshots) and saga states.

* The **subject** is stored in clear: use a stable, pseudonymous id (a customer id), never personal data such as an email. It must not be `null` when the object carries personal data.
* Any field type works (strings, numbers, nested objects, lists). A `null` field stays `null`.
* Fields only: not getters, not record components. The `@DataSubject` is the one of the object that has the field; a nested object with personal data has its own `@DataSubject`.
* Data written before a field was marked is read as it is.

## Forgetting a subject

From a bundle, for example in the service that handles an erasure request:

```java
@CommandHandler
CustomerForgotten handle(ForgetCustomer command) {
    SubjectKeys.forget(command.getCustomerId());
    return new CustomerForgotten(command.getCustomerId());
}
```

Or from the server, as an administrator (recorded in the audit trail):

```
DELETE /api/personal-data/subjects/{subject}
```

From then on every `@PersonalData` field of that subject reads as `null` (or `0`/`false` for primitives): aggregates rebuilt from their events, projectors replayed from the start, everything. Write your aggregates and projectors so that they tolerate it.

{% hint style="warning" %}
Erasure covers what Evento stores. **Read models** (projections in your databases) that copied personal data in clear are yours to clean: publish an event such as `CustomerForgotten` and let the projectors delete or anonymize their rows. Logs, emails sent and external systems are outside the event store too.
{% endhint %}

A subject written again after being forgotten gets a new key: the new data is readable, the old stays unreadable.

## Where the keys are

The keys are kept by the Evento servers in the event store's database (table `es__subject_keys`), so every server and every bundle sees the same key, and a cluster needs no extra component. Bundles ask for them over the bus and keep them in memory for a minute, so reading many events does not ask once per event:

```java
EventoBundle.Builder.builder()
        .setSubjectKeyCacheTtl(Duration.ofSeconds(30))   // default one minute; zero asks every time
```

A subject forgotten through one bundle (or the console) can still be read for that long by the other bundles that had its key in memory.

**Protect the keys at rest.** Set the same master key on every server, and the table alone no longer opens the data:

```
EVENTO_SERVER_PERSONAL_DATA_MASTER_KEY=<base64 of 32 random bytes>   # openssl rand -base64 32
```

Without it the keys are stored as they are, and the server logs a warning when it creates the first one. Keys created before the master key was set keep working.

{% hint style="info" %}
**Backups.** A backup of the event store taken before a subject was forgotten still contains that subject's key, and with it the data. Keep backups of `es__subject_keys` no longer than your erasure obligations allow (or back it up separately with a shorter retention): once the last copy of the key is gone, the data is gone everywhere.
{% endhint %}

The server creates the table itself when it manages its schema (`spring.sql.init.mode=always`, the default). With `spring.sql.init.mode=never`, apply `db/upgrade/subject-keys.sql` from the server's resources.

## In tests

The `evento-test` fixtures keep keys in memory, and so does `EventoTestBroker`: nothing to configure. To check erasure in a fixture, install your own provider and forget the subject:

```java
var keys = new InMemorySubjectKeyProvider();
SubjectKeys.install(keys);
// ... given/when ...
keys.forget("c-1");
```

## Upgrading

Personal data needs 3.0 servers (the key requests) and 3.0 bundles everywhere the data is read: a 2.x bundle cannot read an encrypted field (a text field shows the encrypted string). Upgrade the servers, then every bundle that reads those events, then mark the fields.
