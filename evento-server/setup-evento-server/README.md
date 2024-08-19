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
* **evento\_file\_upload\_dir:** Specify the directory where uploaded bundle files will be stored on the server.
* **evento\_security\_signing\_key:** A critical security measure. This JWT (JSON Web Token) signature key is used for signing API requests, ensuring data integrity and authorization. **Never share this key publicly.**
* **evento\_deploy\_spawn\_script:** (Optional) If you intend to automate bundle deployment, provide the path to a Python script that handles the spawning of new bundle instances.
* **spring\_datasource\_url:** The connection URL for your PostgreSQL database.
* **spring\_datasource\_username:** The username for accessing the PostgreSQL database.
* **spring\_datasource\_password:** The password for accessing the PostgreSQL database.

**Important Note:** The `evento_security_signing_key` should be treated as a secret and not be included in any public documentation or version control systems.

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
    privileged: true  # Grant necessary privileges for file uploads (optional, consider alternatives)
    depends_on:
      - database  # Ensure database is ready before starting Evento Server
    environment:
      - evento_cluster_name=evento-server  # Set your cluster name
      - evento_performance_capture_rate=0.1  # Capture telemetry data every 0.1 seconds (adjust as needed)
      - evento_telemetry_ttl=365  # Keep telemetry data for a year
      - evento_file_upload_dir=/server_upload  # Upload directory on the server
      - evento_security_signing_key=MY_JWT_SECRET_TOKEN_SEED  # Replace with a strong secret
      # (Optional) Path to your deployment script if using automated bundle deployment
      - evento_deploy_spawn_script=/script/spawn.py 
      - spring_datasource_url=jdbc:postgresql://database:5432/evento
      - spring_datasource_username=postgres
      - spring_datasource_password=secret  # Replace with your actual password
    ports:
      - '3000:3000'  # Map container port 3000 to host port 3000 (default Evento Server port)
      - '3030:3030'  # Map container
```
