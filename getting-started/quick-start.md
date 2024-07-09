---
description: Evento Server and Evento Framework
---

# Quick Start

## Evento Server

To start building a RECQ based Architecture you need a Message Gateway to handle and manage message communication between components (microservices). To do this we use [Broken link](broken-reference "mention").

To start using Evento Server you need a [Postgres Database](https://www.postgresql.org/) and an instance of Evento Server that you can find on [Docker Hub](https://hub.docker.com/):  [https://hub.docker.com/r/eventoframework/evento-server](https://hub.docker.com/r/eventoframework/evento-server)

We have also prepared a simple docker-compose.yml to set up your development environment:

```yaml
version: '3.3'
services:
  evento-db:
    image: 'postgres:latest'
    restart: always
    environment:
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=evento
    volumes:
      - ./data/postgres:/var/lib/postgresql/data/
  evento-server:
    image: 'eventoframework/evento-server:latest'
    privileged: true
    restart: on-failure
    depends_on:
      - evento-db
    environment:
      # Cluster name visualized on the GUI
      - evento_cluster_name=evento-server
      # Capture rate for internal telemetry
      - evento_performance_capture_rate=1
      # Telemetry data TTL
      - evento_telemetry_ttl=365
      # Upload directory for Bundle Registration
      - evento_file_upload-dir=/server_upload
      # Secret key used to generate JWT access tokens
      - evento_security_signing_key=MY_JWT_SECRET_TOKEN_SEED
      # Evento Deploy Spawn Script Path
      - evento_deploy_spawn_script=/script/spawn.py
      # Postgres Database Connection Parameters
      - spring_datasource_url=jdbc:postgresql://evento-db:5432/evento
      - spring_datasource_username=postgres
      - spring_datasource_password=secret
    ports:
      - '3000:3000'
      - '3030:3030'
    volumes:
      - ./data/evento/files:/server_upload
      - ./docker-spawn.py:/script/spawn.py
```

You need to specify a Script for the automatic bundle deployment, add an empty Python script and bind it, it will be fine at the start.

***

## Evento Framework

To develop RECQ components you need the [Broken link](broken-reference "mention") Bundle Library.

{% hint style="danger" %}
Evento Framework is compatible with[ Java 21](https://openjdk.org/projects/jdk/21/) or more.
{% endhint %}

You can find the library on [Maven Central](https://central.sonatype.com/):  [https://central.sonatype.com/artifact/com.eventoframework/evento-bundle](https://central.sonatype.com/artifact/com.eventoframework/evento-bundle)

#### Gradle

```gradle
implementation group: 'com.eventoframework', name: 'evento-bundle', version: 'ev1.9.0'
```

#### Maven&#x20;

```xml
<dependency>
    <groupId>com.eventoframework</groupId>
    <artifactId>evento-bundle</artifactId>
    <version>ev1.9.0</version>
</dependency>
```



{% hint style="info" %}
Evento framework is independent of any other structured known framework like [Spring](https://spring.io/), [Micronaut ](https://micronaut.io/)or [Quarkus](https://quarkus.io/), so you can implement a RECQ application using your preferred technology even plain [JavaEE](https://it.wikipedia.org/wiki/Jakarta\_EE).
{% endhint %}

***

Tu understands how to use properly Evento Server and Evento Framework we suggest you follow our Tutorial in the next chapter.
