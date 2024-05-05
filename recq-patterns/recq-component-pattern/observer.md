---
description: Component like Saga but does not hold a state and has no order constraints.
---

# Observer

<figure><img src="../../.gitbook/assets/image (45).png" alt=""><figcaption><p>RECQ Observer Big Picture</p></figcaption></figure>

While a saga must have an internal state in order to understand how to move a transaction forward, an Observer (Observer) has no historical memory and reacts to a single event.

It has the usual "on" method (Event Handler) which, like the Projector, depends on a single event and returns nothing, however, an Observer can make Command and Query type requests like the sagas.

In reality, an Observer is a special case of a saga that begins and ends with a single event.

Its behaviour is also comparable to a service that is invoked from within via an event.

Not having an internal state it can scale easily, furthermore, unlike the implementation of sagas or projectors, for an observer there is no orderly and consistent consumption constraint of the events.

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | No  |
| Can handle Query Messages   | No  |
| Can handle Events           | Yes |
| Can send Command Messages   | No  |
| Can Send Query Messages     | Yes |
| State type                  | No  |
| CAP Properties              | AP  |

<figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption><p>Observer Structure</p></figcaption></figure>
