---
description: Bus authentication and TLS, payload allowlist, and the production profile
---

# Security

A single property tells the server whether it runs in development or in production, and the server refuses to start in production while a piece of hardening is missing.

## The security profile

```properties
evento.server.security.profile=prod     # EVENTO_SERVER_SECURITY_PROFILE
```

* `prod`, **the default**, does not start, before opening the bus port, until every check passes, and lists the failing ones.
* `dev` logs at startup the checks that fail (`event=security_profile_dev`) and starts: for development, tests and demos (`EVENTO_SERVER_SECURITY_PROFILE=dev`).

| Check | How to pass it |
|---|---|
| Bundles must authenticate | `evento.server.bus.auth-token` (`EVENTO_SERVER_BUS_AUTH_TOKEN`) |
| The bus is encrypted | `evento.server.bus.tls.enabled=true` and its certificates (below) |
| Payload deserialization is restricted | `EVENTO_SERIALIZATION_ALLOWED_PACKAGES` (below) |
| The console password is not the shipped one | `SPRING_SECURITY_USER_PASSWORD` other than `secret` |
| The database password is not the shipped one | `SPRING_DATASOURCE_PASSWORD` other than `secret` |
| The REST API does not accept any origin | `EVENTO_SERVER_WEB_CORS_ALLOWED_ORIGINS` without `*` |

{% hint style="info" %}
Evento 3.0 plans `prod` as the default.
{% endhint %}

## Bundle authentication

Set a shared secret on the server and the same on every bundle:

```properties
# server
evento.server.bus.auth-token=${EVENTO_SERVER_BUS_AUTH_TOKEN}
```

```java
// bundle
EventoBundle.Builder.builder().setAuthToken(System.getenv("EVENTO_BUNDLE_AUTH_TOKEN"))
```

With the [Spring Boot Starter](../../evento-framework/eventobundle/spring-boot-starter.md): `evento.bundle.auth-token`. A bundle without the right token is refused at the handshake.

## TLS and mutual TLS on the bus

The server reads PEM files (the private key in PKCS#8; convert a `BEGIN RSA PRIVATE KEY` file with `openssl pkcs8 -topk8 -nocrypt`):

```properties
evento.server.bus.tls.enabled=true
evento.server.bus.tls.cert-chain=/etc/evento/server.pem
evento.server.bus.tls.private-key=/etc/evento/server.key
# mutual TLS: bundles need a certificate signed by one of these CAs
evento.server.bus.tls.trust-certs=/etc/evento/bundles-ca.pem
evento.server.bus.tls.client-auth=require     # none | optional | require
```

Every property also exists as an environment variable (`EVENTO_SERVER_BUS_TLS_ENABLED`, `..._CERT_CHAIN`, `..._PRIVATE_KEY`, `..._PRIVATE_KEY_PASSWORD`, `..._TRUST_CERTS`, `..._CLIENT_AUTH`). TLSv1.3 and TLSv1.2 are enabled. A missing or unreadable file stops the server at startup.

A bundle connects with TLS through its transport configuration, or with the starter's `evento.bundle.tls.*`:

```java
var tls = SslContextBuilder.forClient()
        .trustManager(new File("/etc/evento/server-ca.pem"))
        .keyManager(new File("/etc/evento/bundle.pem"), new File("/etc/evento/bundle.key")) // mutual TLS
        .build();
EventoBundle.Builder.builder().setTransportConfig(NettyTransportConfig.defaults().withSslContext(tls))
```

TLS authenticates the channel, the token authorizes the bundle: production uses both.

## Payload allowlist

Evento stores and transmits payloads with their class name, and Jackson instantiates the class it reads. Left open, any `Serializable` class on the classpath can be named, which is the classic deserialization gadget risk. Restrict it to your packages:

```properties
EVENTO_SERIALIZATION_ALLOWED_PACKAGES=com.acme.orders,com.acme.shared.api
```

Then only `com.evento.*`, the JDK value types (`java.util`, `java.time`, `java.math`) and those packages are accepted; anything else is refused before its class is loaded. The server needs it too, since it reads stored payloads. On a bundle, `setRestrictPayloadTypes(true)` allows its base package, and `setAllowedPayloadPackages(...)` more (starter: `evento.bundle.serialization.*`).

## A complete example: the live demo

The [live demo](https://www.eventoframework.com/demo/) runs the `prod` profile in public, with one Docker Compose file ([`docker-compose.prod.yml`](https://github.com/EventoFramework/evento-www/blob/main/docker-compose.prod.yml)). The server:

```yaml
evento-server:
  image: eventoframework/evento-server:3.0.0
  environment:
    EVENTO_SERVER_SECURITY_PROFILE: prod
    EVENTO_SERVER_BUS_AUTH_TOKEN: ${EVENTO_BUS_TOKEN}            # openssl rand -hex 32
    EVENTO_SERVER_BUS_TLS_ENABLED: "true"
    EVENTO_SERVER_BUS_TLS_CERT_CHAIN: /certs/bus.crt
    EVENTO_SERVER_BUS_TLS_PRIVATE_KEY: /certs/bus.key           # PKCS#8
    EVENTO_SERIALIZATION_ALLOWED_PACKAGES: com.eventoframework.demo.todo
    EVENTO_SERVER_WEB_CORS_ALLOWED_ORIGINS: https://gui.eventoframework.com
    EVENTO_SERVER_PERSONAL_DATA_MASTER_KEY: ${EVENTO_PERSONAL_DATA_MASTER_KEY}   # openssl rand -base64 32
    spring_datasource_password: ${DEMO_DB_PASSWORD}
    SPRING_SECURITY_USER_NAME: guest
    SPRING_SECURITY_USER_PASSWORD: ${GUI_PASSWORD}
    SPRING_SECURITY_USER_ROLES: WEB                               # reads the console, changes nothing
  volumes:
    - ./deploy/tls:/certs:ro
```

and the bundle, a Spring Boot application with the starter:

```properties
evento.bundle.servers=evento-server:3030
evento.bundle.auth-token=${EVENTO_BUNDLE_AUTH_TOKEN}
evento.bundle.tls.enabled=true
evento.bundle.tls.trust-certs=/certs/bus.crt
evento.bundle.serialization.restrict=true
```

The bus is reachable only on the Compose network, so a self-signed certificate for the internal name `evento-server` is enough:

```bash
openssl req -x509 -newkey rsa:3072 -nodes -days 3650 -subj "/CN=evento-server" \
  -addext "subjectAltName=DNS:evento-server" -keyout bus-rsa.key -out bus.crt
openssl pkcs8 -topk8 -nocrypt -in bus-rsa.key -out bus.key
```

The server logs `event=security_profile profile=prod checks=passed` and `event=bus_tls_enabled` when it starts. The public guest can read every page of the console; a change it attempts is refused (403) and recorded in the [audit trail](../../evento-gui/gui-auth.md).
