---
description: >-
  Component that also implements the pattern's Command Model CQRS extension.
  Unlike the aggregate, it does not have a state or its state is external to
  thesystem (not the responsibility of the system)
---

# Service

<figure><img src="../../.gitbook/assets/image (41).png" alt=""><figcaption><p>RECQ Service Big Picture</p></figcaption></figure>

This component also has a command handler, but unlike the aggregate, the latter takes only the command as input and may not return events, other than the fact that cannot make query-type requests.&#x20;

An example of a service would be the component responsible for sending the emails mentioned above. Sending an email is something external to the application system you are on developing, moreover, this action must be available and consistent but the fact of being able whether or not to send the mail does not depend on the information contained in the system. Like the invokers it was the components that bridged the gap between the outside and the inside, the services do the opposite. A further example would be the implementation of a payment service delegated to an external provider, requests to the provider must also be consistent but this consistency is not our responsibility.&#x20;

For scalability aspects, consistency is not taken into account because it is not dependent on the internal system (c) therefore as a whole it is available, except for one of its own ACID implementation, (a) and partitioning tolerant (P).

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | Yes |
| Can handle Query Messages   | No  |
| Can handle Events           | No  |
| Can send Command Messages   | Yes |
| Can Send Query Messages     | No  |
| State type                  | No  |
| CAP Properties              | caP |

<figure><img src="../../.gitbook/assets/image (43).png" alt=""><figcaption><p>Service Structure</p></figcaption></figure>
