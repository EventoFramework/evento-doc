---
description: >-
  Component that can only "invoke" others, it doesn't have an internal state and
  cannot receive messages from within the system.
---

# Invoker

<figure><img src="../../.gitbook/assets/image (39).png" alt=""><figcaption><p>RECQ Invoker Big Picture</p></figcaption></figure>

The invoker is a bridge component between the outside of the system and the inside.&#x20;

An example of an Invoker is a REST controller that exposes system actions for being able to allow access via the network. It can also be a GUI controller, a CLI application or a trigger from CRON.

Having no internal state, this component can scale at will, therefore, it can turn out always available (A) and is partitioning tolerant (P)

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | No  |
| Can handle Query Messages   | No  |
| Can handle Events           | No  |
| Can send Command Messages   | Yes |
| Can Send Query Messages     | Yes |
| State type                  | No  |
| CAP Properties              | AP  |

<figure><img src="../../.gitbook/assets/image (44).png" alt=""><figcaption><p>Invoker Structure</p></figcaption></figure>
