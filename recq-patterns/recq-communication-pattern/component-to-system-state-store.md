---
description: Synchronous Event Posting
---

# Component to System State Store

In a RECQ architecture, components interact with the System State Store (SSS) in a specific manner for managing state changes. This interaction follows a request/response pattern with a synchronous protocol managed by the SSS itself.

**Communication Protocol:**

* **Synchronous Event Posting:** Unlike the asynchronous communication used for component-to-component interaction, posting a state change event to the SSS is a synchronous operation.
  * Components send a request message directly to the SSS containing the event data representing the desired state change.
  * The SSS validates the event and attempts to persist it in its storage mechanism.
  * Upon successful persistence, the SSS sends a response message back to the component, confirming the success or failure of the operation.
  * The synchronous nature ensures the component receives confirmation before proceeding with further actions that might depend on the state change.

<figure><img src="../../.gitbook/assets/image (27).png" alt=""><figcaption></figcaption></figure>

**Benefits of Synchronous Event Posting:**

* **Strong Consistency:** Synchronous event posting guarantees that the event is successfully persisted in the SSS before the component receives a confirmation. This ensures strong consistency between the component's view of the state and the actual state stored in the SSS.
* **Simplified Error Handling:** The component receives immediate feedback on the success or failure of the event posting, allowing for easier error handling and potential retries if necessary.

**Considerations:**

* **Reduced Scalability:** Synchronous communication can introduce bottlenecks if a large number of components frequently update the state. This might require careful configuration and optimization of the SSS to handle high volumes of event posting requests.
* **Potential Latency:** If components rely heavily on immediate confirmation, synchronous event posting can introduce slight latency compared to asynchronous approaches.

**Conclusion:**

The RECQ architecture utilizes a synchronous request/response pattern for component-to-SSS communication when posting state change events. This approach guarantees strong consistency and simplifies error handling, but it's important to consider potential scalability and latency impacts for high-volume systems. The specific communication strategy might be adjusted based on the application's specific needs and performance requirements.
