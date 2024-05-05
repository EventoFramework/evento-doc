# Component to Component

Communication from one component to another component is implemented with a protocol of asynchronous requests and responses from the [Message Gateway](../recq-system-pattern/message-gateway.md).

However, each component can only send two types of messages:&#x20;

* Commands – a request to a system change action which, in response, will only have confirmation of whether or not the action has taken place.
* Query – a request that does not change the system, but returns the data (the views or View)

This is because the components must obey the CQRS pattern.

<figure><img src="../../.gitbook/assets/image (19).png" alt=""><figcaption><p>Component to Component Communication</p></figcaption></figure>
