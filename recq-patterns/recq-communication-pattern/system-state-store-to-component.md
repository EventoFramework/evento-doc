# System State Store to Component

The communication takes place with a [pub/sub protocol](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe\_pattern) managed not by the[ Message Gateway](../recq-system-pattern/message-gateway.md) but from the combination of the [System State Store](../recq-system-pattern/system-state-store.md) and the [Consumer State Stores](../../evento-framework/bundle/consumer-state-store.md) (for le [Sagas ](../recq-component-pattern/saga.md)and [Projections](../recq-component-pattern/projection.md)).&#x20;

<figure><img src="../../.gitbook/assets/image (48).png" alt=""><figcaption><p>System STate Store to Component Communication</p></figcaption></figure>

[Consumer State Stores](../../evento-framework/bundle/consumer-state-store.md) are modules that aim to make the state persistent progress of event consumption from the SSS, so as to implement retry logics e ensure orderly progress and consistency.
