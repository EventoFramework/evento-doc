# GUI Auth

#### Signing In: Username and Password

When you open the Evento GUI, you are greeted by a branded login page. Authentication uses a standard **username and password** over **HTTP Basic auth** — there are no tokens to generate, no application logs to scrape, and no token expiry.

<figure><img src="../.gitbook/assets/image (52).png" alt=""><figcaption><p>The Evento GUI login page</p></figcaption></figure>

The credentials are the ones configured on the Evento Server through Spring Boot's in-memory user:

* `spring.security.user.name` — the login username (default: `evento`)
* `spring.security.user.password` — the login password (default: `secret`)

{% hint style="warning" %}
The defaults (`evento` / `secret`) are for local exploration only. **Always override both properties in any real deployment**, e.g. by setting the `SPRING_SECURITY_USER_NAME` and `SPRING_SECURITY_USER_PASSWORD` environment variables on the server container.
{% endhint %}

#### How It Works

* The login page verifies your credentials directly against the server; on success you land on the dashboard.
* The GUI attaches the credentials as an `Authorization: Basic` header to every API call, and caches them in the browser's localStorage so the session survives page reloads.
* If the server ever rejects your credentials (401) — for example after the password is changed — the GUI clears the stored credentials and redirects you back to the login page.
* If you are signed in but lack the role an action needs (403), the GUI tells you so ("This action needs the ADMIN role.") and keeps you signed in.
* Use the **logout** button in the header to clear the stored credentials at any time.

#### Single Sign-On with OpenID Connect

Since Evento **3.0** the console can sign users in through your organisation's identity provider (Keycloak, Entra ID, Okta, Google Workspace, …) instead of the shared user:

```properties
evento.server.web.auth=oidc                                   # EVENTO_SERVER_WEB_AUTH
spring.security.oauth2.client.registration.evento.client-id=evento-console
spring.security.oauth2.client.registration.evento.client-secret=${OIDC_CLIENT_SECRET}
spring.security.oauth2.client.registration.evento.scope=openid,profile,email
spring.security.oauth2.client.provider.evento.issuer-uri=https://login.example.com/realms/acme
# which groups grant the console's roles
evento.server.web.oidc.roles-claim=groups                     # e.g. roles (Entra ID), realm_access.roles (Keycloak)
evento.server.web.oidc.web-role=evento-web                    # read the console
evento.server.web.oidc.admin-role=evento-admin                # also consumer operations
```

Register the console at the provider as a confidential web client with the redirect URI `https://<your-server>/login/oauth2/code/evento`.

* The login page shows **Sign in with your organisation**: the server runs the authorization-code flow (with PKCE) and brings you back to the dashboard.
* The session lives in an HttpOnly cookie; no token reaches the browser. Changes (consumer operations) carry a CSRF token the GUI reads from the `XSRF-TOKEN` cookie.
* A user whose groups grant neither role can sign in but sees nothing (every API call answers 403).
* HTTP Basic stays available for machine clients, e.g. a Prometheus scrape of `/actuator/prometheus` with the configured user.

#### Roles

* `WEB` reads the console: dashboard, catalog, flows, cluster status, consumers, event store.
* `ADMIN` is needed for every change: retrying, deleting or replaying dead events, and removing a bundle from the catalog (`DELETE /api/bundle/{id}`).

The Basic user gets both roles; with OIDC they come from the provider's groups.

#### Audit Trail

Since Evento **3.0** the server records who did what in the console (on by default; `management.auditevents.enabled=false` turns it off):

| Event | When |
| --- | --- |
| `ADMIN_ACTION` | every change, with the action, its target, the caller's address and the outcome (`ok`, or `failed` with the error), written when the bundle has answered |
| `AUTHENTICATION_FAILURE` | a wrong password, a failed OIDC sign-in |
| `AUTHENTICATION_SUCCESS`, `LOGOUT` | OIDC sign-in and sign-out (Basic re-authenticates on every request, so its successes are not recorded) |
| `AUTHORIZATION_FAILURE` | a signed-in user refused an action its roles do not grant |

Each event is one line on the `evento.audit` logger:

```
event=audit type=ADMIN_ACTION principal=alice action=consumer.dead_queue.consume consumerId=orders_OrderProjector_1_default remoteAddress=10.0.4.17 outcome=ok
```

That log is the durable record: route the `evento.audit` logger to your SIEM or to an append-only file. The latest events (`evento.server.audit.capacity`, default 1000) are also at `/actuator/auditevents`, for `ADMIN` users only; they are kept in memory and lost on restart. `management.auditevents.enabled=false` turns the audit off.

#### Scope of Authentication

All GUI pages and every `/api/**` endpoint require authentication; only the health/info actuator probes are public. Note that this login protects the **web GUI and REST API**. Bundle connections on the message bus are authenticated separately with the optional wire-level shared secret (`evento.server.bus.auth-token`, see [Advanced Options](../evento-server/setup-evento-server/advanced-options.md)).
