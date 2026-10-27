---
description: Serving several tenants with Evento, in one application or in one installation per tenant
---

# Multi-Tenancy

Evento has no tenant setting, by design. A tenant is either a concept of your domain (the customers of a SaaS application, sharing one installation) or a reason to run separate installations (customers who must not share anything). Both work with Evento as it is; this page shows how, and why the framework does not add a third way.

| | Shared installation, tenant in the domain | One installation per tenant (silo) |
|---|---|---|
| Isolation | Logical: your code keeps tenants apart | Physical: separate servers, databases, credentials |
| Cost per tenant | None | One server cluster and one database each (servers are light) |
| Cross-tenant views (billing, support) | One projection | Aggregated outside |
| Erasing a tenant | Forget its subjects, clean its rows | Drop its database |
| Good for | Many small tenants, one product | Few large or regulated tenants, data residency |

## Tenant as a concept of the domain

All tenants share the servers, the event store and the bundles; every message says which tenant it belongs to.

**Put the tenant in the identity.** Aggregate ids are global in the event store: make them carry the tenant, so two tenants never address the same aggregate, and the aggregate lock (which follows the aggregate id by default) never makes one tenant wait for another.

```java
public class PlaceOrder extends DomainCommand {
    String tenantId;
    String orderId;

    @Override
    public String getAggregateId() {
        return tenantId + ":" + orderId;
    }
}
```

**Put the tenant in the payloads**, commands, events and queries alike, as a field: it is the source of truth that handlers check, and it survives replays and upcasting. Metadata is fine for cross-cutting information (who asked, from which channel), not for the tenant a handler must enforce.

**Check it where the decision is taken.** The aggregate refuses a command for another tenant's order (`state.tenantId` against `command.tenantId`); query handlers filter by the tenant of the query; your API layer takes the tenant from the authenticated user, never from the request body.

**Idempotency keys are global too**: derive them from the tenant as well (`tenantId + ":" + requestId`), or two tenants using the same request id would see each other's replay.

**Read models** carry a tenant column and every query filters on it, as in any multi-tenant database. A projector that serves only some tenants can read only their events by giving events a [context](eventobundle/context.md) per tenant (or per group of tenants) and starting one consumer per context:

```java
// in the aggregate
return new OrderPlaced(command.tenantId, command.orderId, ...).setContext(command.tenantId);

// in the bundle that serves tenants acme and globex
EventoBundle.Builder.builder()
        .setComponentContexts(OrderProjector.class, "acme", "globex")
```

Each context has its own checkpoint, so a slow or failing tenant does not hold up the others, and a tenant's read model can be rebuilt alone. With many tenants, use contexts per group (a region, a plan) rather than per tenant: every context is a consumer.

**Personal data** works per data subject, not per tenant: use subject ids that include the tenant (`acme:customer-42`) and forget them one by one when a tenant leaves (see [Personal Data](personal-data.md)).

## One installation per tenant (silo)

When tenants must not share infrastructure (contracts, regulators, data residency, very different load), run one Evento installation per tenant: its own servers, its own database, its own bus token and credentials. Nothing in Evento changes, and nothing can leak between tenants because nothing is shared.

* Give each tenant **its own database**. Several databases can live on one PostgreSQL instance; avoid putting tenants in separate schemas of one database, because the servers' advisory locks (the event store lock among them) are per database, so tenants would wait for each other.
* Give each installation **its own bus auth token and TLS identity**, and its own console users.
* Deploy **the bundles per tenant** too, pointed at their tenant's servers. The same image with a different configuration is enough.
* Upgrades go tenant by tenant, which also gives you a natural canary.

## Why not in the framework

The only thing the framework could add is a shared installation in which the server itself keeps tenants apart: bundles authenticated per tenant, every fetch filtered, every command and query checked, the catalog, consumers, locks, idempotency keys, keys of data subjects and the console split by tenant. That is a security boundary through every path of a component built for the bundles of one application, and its only users are those who run Evento as a platform for other companies' applications, which is the use the [licence](../licensing.md) reserves to authorised parties. The two ways above cover the rest without it.
