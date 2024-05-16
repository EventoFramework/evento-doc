# Evento Server Cluster

In the ever-growing landscape of distributed systems, handling increased load and ensuring high availability are paramount concerns. Fortunately, Evento Server offers the capability to be clustered, allowing you to deploy multiple instances for enhanced scalability and fault tolerance.

#### Clustered Architecture: Sharing the Burden

Evento Server can be configured as a cluster, utilizing a shared PostgreSQL database. This approach leverages the Shared Database pattern:

* **Shared Database:** A single PostgreSQL instance serves as the central repository for all cluster members. This database stores configuration, event streams, and other critical data for all Evento Server instances within the cluster.
* **Multiple Evento Server Instances:** You can deploy multiple Evento Server instances, each communicating with the shared PostgreSQL database. This distribution of workload across multiple servers enhances processing power and scalability.

<figure><img src="../.gitbook/assets/image (50).png" alt=""><figcaption></figcaption></figure>

**Alternative: PostgreSQL Cluster**

While the Shared Database pattern is a viable option, you can also leverage a dedicated PostgreSQL cluster for increased fault tolerance. In this scenario, the Evento Server instances would connect to the cluster endpoint, ensuring data redundancy and availability even if individual PostgreSQL nodes experience failures.

#### Benefits of Clustering:

* **Scalability:** Distribute workload across multiple servers to handle increased message traffic and application complexity.
* **High Availability:** Mitigate the impact of single-point failures. If one Evento Server instance becomes unavailable, others can continue processing messages, minimizing downtime.
* **Improved Performance:** Leverage the combined processing power of multiple servers to enhance overall cluster performance.

#### Setting Up a Cluster:

1. **Deploy Multiple Evento Server Instances:** Use Docker Compose or another container management tool to deploy multiple Evento Server instances. Configure each instance with unique ports to avoid conflicts.
2. **Shared PostgreSQL Configuration:** All Evento Server instances within the cluster need to connect to the same PostgreSQL database. Ensure the connection details (URL, username, password) are consistent across all server configurations.
3. **Evento Bundle Configuration:** When creating your Evento bundles, specify the addresses of all Evento Server instances within the cluster. This allows bundles to communicate with any available server for optimal load balancing and fault tolerance.

**Important Note:** Security considerations are crucial in a clustered environment. Implement appropriate access control mechanisms for the shared PostgreSQL database to ensure data integrity and prevent unauthorized access.

#### Conclusion:

Clustering Evento Server empowers you to build robust and scalable distributed systems. By leveraging multiple servers and a shared database, you can achieve high availability, handle increased load, and ensure smooth operation of your application ecosystem. Remember to prioritize security measures when deploying a clustered environment.
