---
description: >-
  Component that implements the Query Model of the CQRS pattern, but only deals
  with the writing part of the local model.
---

# Projector

<figure><img src="../../.gitbook/assets/image (42).png" alt=""><figcaption><p>RECQ Projector Big Picture</p></figcaption></figure>

It presents an "on" method (called event Handler) which takes an Event as input, ie one of the state changes from the [SSS](../recq-system-pattern/system-state-store.md), and builds the local domain model of the system without returning anything.

Each projector is consistent and processes only one event at a time in sequence, so it cannot scale. In particular, a projector implements the singleton pattern (Gamma, Helm, Johnson, & Vlissides, 1994) at the whole system level.&#x20;

Projectors have an internal state which consists of knowing how far they have consumed from the SSS (to ensure they are consistent with the SSOT up to the time stored) in a Shared Consumer State Store using the Shared Database technique (Richardson, Microservices Patterns: With examples in Java, 2018) by type of projector.&#x20;

The Consumer State Store is a submodule that implements the methods to be able to save the identifier of the last consumed event, return the last consumed event and manage concurrent access to this data.&#x20;

Being within the Query Model, each Event Handler cannot perform actions aimed at changing the state of the system, but can possibly access the data of other components making requests of the Query type even if the answers may not be consistent with the local model.

| Capability                  |           |
| --------------------------- | --------- |
| Can handle Command Messages | No        |
| Can handle Query Messages   | No        |
| Can handle Events           | Yes       |
| Can send Command Messages   | No        |
| Can Send Query Messages     | Yes       |
| State type                  | Component |
| CAP Properties              | CP        |

<figure><img src="../../.gitbook/assets/image (37).png" alt=""><figcaption><p>Projector Structure</p></figcaption></figure>
