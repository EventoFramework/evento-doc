---
description: >-
  The System State Store page provides a comprehensive view of your system's
  event history and current state. It comprises two primary components: the
  Event Store and the Snapshot Store.
---

# System State Store

#### Event Store

<figure><img src="../.gitbook/assets/image (61).png" alt=""><figcaption><p>Event Store Section in System State Store</p></figcaption></figure>

The Event Store is an append-only log that records every change made to the system state. Each entry in the Event Store represents an event, capturing the details of the change that occurred.

**Event Details:**

* **Event Id:** A unique identifier for the event.
* **Name:** The type of event that occurred.
* **Aggregate Id:** The identifier of the aggregate associated with the event.
* **Context:** Additional context information related to the event.
* **Timestamp:** The time when the event occurred.

<figure><img src="../.gitbook/assets/image (62).png" alt=""><figcaption><p>Event Detail</p></figcaption></figure>

By examining the Event Store, you can:

* **Trace System Evolution:** Follow the sequence of events to understand how the system has changed over time.
* **Debug Issues:** Analyze event history to pinpoint the root cause of problems.
* **Audit System Activity:** Review past events for compliance or regulatory purposes.

#### Snapshot Store

<figure><img src="../.gitbook/assets/image (63).png" alt=""><figcaption></figcaption></figure>

The Snapshot Store contains periodic snapshots of the system's state. Snapshots are created to optimize performance by reducing the number of events that need to be processed to rebuild the current state.

<figure><img src="../.gitbook/assets/image (64).png" alt=""><figcaption></figcaption></figure>

While the Event Store provides a complete and immutable record of system changes, the Snapshot Store offers a more efficient way to access the current state of specific aggregates.

**Note:** The Snapshot Store is typically used internally by the system and may not be directly accessible to users.

By understanding the relationship between the Event Store and the Snapshot Store, you can effectively navigate and analyze your system's state. The System State Store is a valuable tool for developers, system administrators, and auditors to gain insights into system behavior and performance.

