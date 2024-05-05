---
description: >-
  A Saga component implements the Saga Pattern to manage distributed
  transactions.
---

# Saga

<figure><img src="../../.gitbook/assets/image (29).png" alt=""><figcaption><p>RECQ Big Picture</p></figcaption></figure>

There are several cases in which two aggregates or services must share information in order to be consistent at the application level. This component is like a projector only that the changes are made on the system itself.

It has an "on" method (in this case called Saga Event Handler) which, taking the current state of the saga and an Event as input, returns the new state of the saga. This method internally can send both command-type and query-type messages

The state of a saga is similar to that of an aggregate, the difference is that the persistence is local and shared among all active instances of a certain saga. While for the aggregate the state is held in the SSS, shared among all, sagas of a particular type using a Saga Shared Consumer State Store following the Shared Database pattern: this sub-module is an extension of the Consumer State Store that implements additional methods to save and retrieve the particular instance of the saga managed by the component (the transaction state).

It also has the same scalability constraints as a projector.

| Capability                  |           |
| --------------------------- | --------- |
| Can handle Command Messages | No        |
| Can handle Query Messages   | No        |
| Can handle Events           | Yes       |
| Can send Command Messages   | No        |
| Can Send Query Messages     | Yes       |
| State type                  | Component |
| CAP Properties              | CP        |

<figure><img src="../../.gitbook/assets/image (31).png" alt=""><figcaption><p>Saga Structure</p></figcaption></figure>
