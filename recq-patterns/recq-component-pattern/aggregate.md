---
description: >-
  An aggregate is a component that implements the Command Model of the CQRS
  pattern. Is defined as such because it is the implementation of a Domain
  Driven Design Aggregate.
---

# Aggregate

<figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption><p>RECQ Aggregate Big Picture</p></figcaption></figure>

This component represents a single instance that is part of our domain and has its own personal status. The state of this instance is reconstructed by doing a replay of events contained in the SSS for this particular aggregate starting from a identifier contained within the received message.&#x20;

An aggregate, therefore, has only one "handle" method (the command handler), which takes in input a particular message of type Command and a State of the aggregate (represented as a sequence of events) and only as a function of these two returns the consequent event of a change of state or an error. The state change event, if returned, comes next published in the SSS.&#x20;

So the aggregates implement the actual domain logic.

A command handler cannot send Query-type requests, as all information required by him to define whether the command is acceptable or not must be present in its state, moreover, as defined previously, the queries are possibly consistent and therefore not usable to define whether the request is consistent with the rest of the system.&#x20;

However, it can carry out commands, since the latter is by definition always consistent and some commands may depend on others to work: for example, the generation of a unique identifier throughout the system, can not by definition be generated knowing only a portion of the system and therefore, this action depends on a command to generate a unique id towards another responsible aggregate.&#x20;

As for scalability, being there is a state that needs to be maintained consistent (C) there is a lock to avoid concurrent access to the same aggregate, therefore not being able to guarantee availability (a) but only partitioning tolerance (P).&#x20;

However, it must be said that the consistency is not at the level of the entire system but is local (Partitioned State) and consequently also the lack of availability is local; therefore, as a whole the system can be both Consistent and partially available (Basic Availability).

| Capability                  |                             |
| --------------------------- | --------------------------- |
| Can handle Command Messages | Yes                         |
| Can handle Query Messages   | No                          |
| Can handle Events           | No                          |
| Can send Command Messages   | Yes                         |
| Can Send Query Messages     | No                          |
| State type                  | Instance (Bu Aggregate Key) |
| CAP Properties              | CaP                         |

<figure><img src="../../.gitbook/assets/image (23).png" alt=""><figcaption><p>Aggregate Structure</p></figcaption></figure>
