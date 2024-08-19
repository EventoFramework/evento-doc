# Evento Event Store Modes: APES and CPES

The Evento Event Store operates in two distinct modes: APES (Available and Partitionable Event Store) and CPES (Consistent and Partitionable Event Store). These modes are fundamentally different in their approach to event sequencing and consistency, each with its own trade-offs.

#### APES Mode

APES prioritizes availability and partition tolerance. It employs a [snowflake algorithm](https://en.wikipedia.org/wiki/Snowflake\_ID) to generate event sequence numbers. To mitigate potential inconsistencies due to network latency and clock skew, a "fetch delay" mechanism is introduced. This delay ensures that events are not fetched immediately after creation, allowing for sufficient time for synchronization across the cluster.

**Key Characteristics:**

* **High Availability:** APES can tolerate failures and continue to process events.
* **Eventual Consistency:** Eventual consistency guarantees that all replicas will eventually converge to the same state, but there might be temporary inconsistencies.
* **Performance:** APES generally offers higher performance due to the lack of strict consistency guarantees.
* **Use Cases:** Ideal for applications that can tolerate some degree of eventual inconsistency and prioritize high throughput.

#### CPES Mode

CPES emphasizes strong consistency and partition tolerance. It utilizes an auto-increment sequence shared across all cluster nodes to generate unique event identifiers. This ensures strict ordering of events across the system.

**Key Characteristics:**

* **Strong Consistency:** Events are processed in the exact order they are generated, providing strong consistency guarantees.
* **Limited Availability:** In high-load scenarios, CPES might experience reduced availability due to contention for the sequence number.
* **Performance:** CPES typically has lower throughput compared to APES due to the overhead of maintaining strong consistency.
* **Use Cases:** Suitable for applications that require strict data integrity and are willing to sacrifice some performance for consistency.

#### CAP Theorem and Trade-offs

The choice between APES and CPES is influenced by the CAP theorem (Consistency, Availability, Partition Tolerance), which states that it's impossible for a distributed system to simultaneously guarantee all three properties.

* **APES:** Prioritizes Availability and Partition Tolerance, sacrificing strong Consistency.
* **CPES:** Prioritizes Consistency and Partition Tolerance, sacrificing Availability in high-load scenarios.

#### Choosing the Right Mode

Selecting the appropriate Event Store mode depends on the specific requirements of your application:

* **High throughput and acceptable eventual consistency:** APES is the preferred choice.
* **Strict data integrity and consistency:** CPES is the recommended option.

It's essential to carefully evaluate the trade-offs between consistency, availability, and performance to make an informed decision. In some cases, it might be possible to combine elements of both modes through hybrid approaches or application-level compensating transactions.

By understanding the fundamental differences between APES and CPES, you can select the optimal Event Store mode for your Evento application.
