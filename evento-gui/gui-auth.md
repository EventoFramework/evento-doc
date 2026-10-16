# GUI Auth

#### Signing In: Username and Password

When you open the Evento GUI, you are greeted by a branded login page. Since Evento Server v2.2, authentication uses a standard **username and password** over **HTTP Basic auth** — there are no tokens to generate, no application logs to scrape, and no token expiry.

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
* If the server ever rejects a request (401/403) — for example after the password is changed — the GUI clears the stored credentials and redirects you back to the login page.
* Use the **logout** button in the header to clear the stored credentials at any time.

#### Single Sign-On with OpenID Connect

Since Evento **2.6** the console can sign users in through your organisation's identity provider (Keycloak, Entra ID, Okta, Google Workspace, …) instead of the shared user:

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

#### Scope of Authentication

All GUI pages and every `/api/**` endpoint require authentication; only the health/info actuator probes are public. Note that this login protects the **web GUI and REST API**. Bundle connections on the message bus are authenticated separately with the optional wire-level shared secret (`evento.server.bus.auth-token`, see [Advanced Options](../evento-server/setup-evento-server/advanced-options.md)).
