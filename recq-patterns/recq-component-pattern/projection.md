---
description: >-
  A component that implements reading aspects of the Query Model of the CQRS
  pattern.
---

# Projection

<figure><img src="../../.gitbook/assets/image (20).png" alt=""><figcaption><p>RECQ Projection Big Picture</p></figcaption></figure>

Projections act as dedicated components responsible for handling queries and delivering relevant data to the application. They leverage the materialized views constructed by Projectors for efficient data retrieval.

**The `QueryHandler` Method: The Power of Query Processing**

Projections expose a single prominent method – the `QueryHandler`. This method takes centre stage when a query message arrives:

* **Query Reception:** The `QueryHandler` receives a query message specifying the data the application needs.
* **Data Retrieval from Materialized View:** The Projection retrieves the requested information from the relevant materialized view, which is typically stored in a database managed by a Projector.
* **Data Transformation and Delivery:** Projections might further process or transform the retrieved data to match the specific format required by the query before sending it back as a response.

<figure><img src="../../.gitbook/assets/image (36).png" alt=""><figcaption><p>Projection Structure</p></figcaption></figure>

**Scalability Unleashed: Stateless Design for High Performance**

Like Projectors, Projections embrace a stateless design. This means they do not maintain any persistent state information about the queries they have processed. This stateless nature allows for horizontal scaling – you can add more Projection instances to handle increasing query loads without compromising consistency.

**Consistency Considerations: Leveraging Materialized Views**

Projections rely on the eventual consistency provided by Projectors and the materialized views they create. This means the data returned by a Projection might not always reflect the absolute latest state changes, as some events might still be propagating through the system. However, this eventual consistency is often acceptable for many read-heavy scenarios, where near real-time data is sufficient.

**Query-Centric and Federated Query Support:**

Projections strictly operate within the Query Model. They cannot directly modify the system state or send Command-type messages. However, they can leverage patterns like Federated Queries to retrieve data from other Projections, even if the underlying materialized views might not be perfectly consistent due to eventual consistency. This approach can still be valuable for complex queries that require data from multiple sources.

**The Synergy Between Projectors and Projections:**

* Projectors act as the workhorses, continuously processing events from the System State Store (SSS) and materializing them into optimized, query-friendly structures within a database.
* Projections, in turn, act as the gateways to this materialized data. They efficiently retrieve and potentially transform the data stored by Projectors to fulfill incoming query requests.

**Projections in Action: Simplifying Data Retrieval with Materialized Views**

By offering a scalable and efficient way to handle queries using materialized views, Projections empower applications to retrieve data rapidly. Their stateless design allows for horizontal scaling, making them well-suited for high-traffic query workloads. While eventual consistency might introduce slight delays in reflecting the latest state changes, Projections often provide an optimal balance between performance and consistency for read-heavy scenarios.

**In essence, Projectors and Projections work in tandem to deliver a robust and scalable approach to managing read models in a RECQ architecture.**

| Capability                  |     |
| --------------------------- | --- |
| Can handle Command Messages | No  |
| Can handle Query Message    | Yes |
| Can handle Events           | No  |
| Can send Command Messages   | No  |
| Can Send Query Messages     | Yes |
| State type                  | No  |
| CAP Properties              | AP  |
