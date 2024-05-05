---
description: >-
  A methodological pattern that explains how components in a RECQ System
  communicate with each other.
---

# RECQ Communication Pattern

We have defined that in a RECQ System all the components cooperates by sending messages, with this pattern we are gonna to define the communication structure based on the expected behavior that each message want to produce inside a RECQ System.

### Messages

In a RECQ System we have messages travelling from a component to an other passing by a Message Gateway. In this section we are gonna to diefine the five type of messages that a RECQ System can handle:

* Commands: Messages in the system that want to change the state of the system
* Events: A consequence of an accepted command that is telling us that the System State has changed
* Queries: Messages to extract data from the system
* View: Messages representing data extracted by a Query (this message is a response)
* Void: A symple response message telling that a Command request has been performed withouth errors (this message is a response)

<figure><img src="../../.gitbook/assets/image (46).png" alt=""><figcaption><p>RECQ Payloads</p></figcaption></figure>

So, the message bus can only handle this kind of messages and each of it with a particular behavior.

### Message Handling

In the next chapters we will explain how those messages are handled and wich communication protocol is applied for every of them:

* [Component to Component:](component-to-component.md) the request/response communication solution to obtain data and performa changes
* [Component to System State Store](component-to-system-state-store.md): How the system state store is updated
* [System State Store to Component](../recq-system-pattern/system-state-store.md): the pub/sub communication solution to distribute system changes across componente
