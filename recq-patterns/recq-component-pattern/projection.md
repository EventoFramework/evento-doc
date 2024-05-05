---
description: >-
  A component that implements reading aspects of the Query Model of the CQRS
  pattern.
---

# Projection

<figure><img src="../../.gitbook/assets/image (20).png" alt=""><figcaption><p>RECQ Projection Big Picture</p></figcaption></figure>

It only presents a "handle" method (in this case defined as Query Handler), then it receives Query type messages to which it replies with the data stored in the structures local data held by the Projector and can scale as you like since it has no state and the state of the local model is asserted to be consistent.&#x20;

Again, the Query Handler, due to the same constraint mentioned above, cannot send requests of type Command, but only Queries to implement patterns such as Federated Query, but even then there is a possibility that data from other projections are not consistent with the local model.

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | No  |
| Can handle Query Message    | Yes |
| Can handle Events           | No  |
| Can send Command Messages   | No  |
| Can Send Query Messages     | Yes |
| State type                  | No  |
| CAP Properties              | AP  |

<figure><img src="../../.gitbook/assets/image (36).png" alt=""><figcaption><p>Projection Structure</p></figcaption></figure>
