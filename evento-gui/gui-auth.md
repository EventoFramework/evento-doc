# GUI Auth

#### Signing In: Username and Password

When you open the Evento GUI, you are greeted by a branded login page. Since Evento Server v2.2, authentication uses a standard **username and password** over **HTTP Basic auth** — there are no tokens to generate, no application logs to scrape, and no token expiry.

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

#### Scope of Authentication

All GUI pages and every `/api/**` endpoint require authentication; only the health/info actuator probes are public. Note that this login protects the **web GUI and REST API**. Bundle connections on the message bus are authenticated separately with the optional wire-level shared secret (`evento.server.bus.auth-token`, see [Advanced Options](../evento-server/setup-evento-server/advanced-options.md)).
