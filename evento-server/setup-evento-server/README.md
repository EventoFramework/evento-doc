# SetUp Evento Server

Evento Server lies at the heart of your distributed system built with the Evento framework. This chapter guides you through the process of installing and configuring an Evento Server instance, enabling you to orchestrate message flow, event processing, and resource management within your cluster.

#### Prerequisites:

* **Docker:** Ensure you have Docker installed and running on your system. You can download and install Docker from the official website ([https://www.docker.com/](https://www.docker.com/)).
* **Docker Compose:** Consider using Docker Compose for easier multi-container management. Instructions for installing Docker Compose can be found on the official website ([https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)).
* **PostgreSQL Database:** Evento Server relies on a PostgreSQL database for data persistence. You can either set up a dedicated PostgreSQL instance or leverage Docker for a convenient solution.

#### Deployment using Docker Image:

The recommended approach for deploying Evento Server is through the official Docker image: `eventoframework/evento-server:latest`. This image contains all the necessary dependencies pre-packaged for a streamlined setup.

#### Configuration Properties:

To customize the behavior of your Evento Server instance, you'll need to define a set of essential properties:

* **evento\_cluster\_name:** A unique identifier for your cluster. Choose a descriptive name to easily distinguish your cluster.
* **evento\_performance\_capture\_rate:** This value determines the frequency at which internal telemetry data is captured. A lower value captures data more frequently, providing more detailed insights but potentially impacting performance.
* **evento\_telemetry\_ttl:** This property defines the global time-to-live for telemetry data stored in days. Data older than this duration will be automatically removed.
* **spring\_security\_user\_name / spring\_security\_user\_password:** The username and password protecting the GUI and REST API (HTTP Basic auth). Defaults are `evento` / `secret` — **always override them in any real deployment.**
* **evento\_server\_bus\_auth\_token** (optional)**:** A shared secret that connecting bundles must present on the message bus. Leave unset to accept any bundle (default).
* **spring\_datasource\_url:** The connection URL for your PostgreSQL database.
* **spring\_datasource\_username:** The username for accessing the PostgreSQL database.
* **spring\_datasource\_password:** The password for accessing the PostgreSQL database.

**Important Note:** Credentials such as `spring_security_user_password` and `evento_server_bus_auth_token` should be treated as secrets and not be included in any public documentation or version control systems.

#### Sample Deployment with Docker Compose:

The provided Docker Compose configuration demonstrates a straightforward approach to deploying Evento Server alongside a PostgreSQL database:

```yaml
version: '3.3'
services:
  database:
    image: 'postgres:latest'
    environment:
      - POSTGRES_PASSWORD=secret  # Replace with your actual password
      - POSTGRES_DB=evento
    volumes:
      - ./data/postgres:/var/lib/postgresql/data/  # Persistent storage for database
    ports:
      - "5433:5432"  # Map container port 5433 to host port 5432

  evento-server:
    image: 'eventoframework/evento-server:latest'
    depends_on:
      - database  # Ensure database is ready before starting Evento Server
    environment:
      - evento_cluster_name=evento-server  # Set your cluster name
      - evento_performance_capture_rate=0.1  # Capture telemetry data every 0.1 seconds (adjust as needed)
      - evento_telemetry_ttl=365  # Keep telemetry data for a year
      - spring_security_user_name=evento  # GUI/API login user
      - spring_security_user_password=secret  # Replace with a strong password
      - spring_datasource_url=jdbc:postgresql://database:5432/evento
      - spring_datasource_username=postgres
      - spring_datasource_password=secret  # Replace with your actual password
    ports:
      - '3000:3000'  # Map container port 3000 to host port 3000 (default Evento Server REST/GUI port)
      - '3030:3030'  # Map container port 3030 (bundle message-bus port)
```

{% hint style="info" %}
**Changed in Evento v2.** Bundles are no longer uploaded to the server as JARs. They register themselves at runtime over the message bus (self-discovery), so there is no upload directory, no `privileged: true`, and no deployment script. Deploying and scaling bundle instances is owned by your orchestrator (e.g. Kubernetes or Nomad).
{% endhint %}
