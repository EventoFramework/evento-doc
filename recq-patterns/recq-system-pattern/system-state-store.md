---
description: >-
  The System State Store (SSS) is the module responsible for persistently
  maintaining the state of the system.
---

# System State Store

The state of the system is represented by the ordered sequence of change-of-state events; this module is to all intents and purposes an **Event Store**.

This module is our system's **Single Source of Truth (SSOT)**. It is the only system component that actually knows the state throughout its history, any other local representation of the system state is a reference.\
Components can be notified of state change events from this module.

The SSS must exhibit the following actions:

* **Publishing a domain event** – then adding a new state change event to the event store, the event can be associated with an aggregate.
* **Get an event Stream** – get all ordered events from a starting point, which can also be filtered by aggregate and type of event.

<figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption><p>System State Store Structure</p></figcaption></figure>
