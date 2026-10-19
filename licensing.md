---
description: Apache-2.0 client libraries, AGPL-3.0 or commercial server
---

# Licensing

Since Evento **2.6** the framework has two licences, one for what your application links and one for what you run next to it.

| Component | Licence |
|---|---|
| Client libraries: `evento-bundle`, `evento-common`, `evento-transport-api`, `evento-transport-netty`, `evento-consumer-state-store-jdbc`, `evento-spring-boot-starter`, `evento-opentelemetry`, `evento-test` | **Apache-2.0** |
| Evento Server and the web console | **AGPL-3.0**, or the **commercial licence** |
| Evento Enterprise: single sign-on (OpenID Connect) and audit trail for the console | **commercial licence** only |

* **Your application** depends only on the client libraries: it carries no copyleft, whatever its own licence.
* **The server** runs next to your bundles, which talk to it over the network. Running it unmodified does not put your applications under the AGPL. If you modify the server and let users interact with it over a network, the AGPL asks you to offer them your changes.
* **The commercial licence** is for organisations that cannot accept the AGPL for the server, or want warranties, indemnification and support. It also gives access to **Evento Enterprise**, a separate server distribution with the console's enterprise features ([GUI Auth](evento-gui/gui-auth.md)); the open-source server has the extension points they use, not the features. See [eventoframework.com/licensing](https://www.eventoframework.com/licensing/).

The client libraries run on **Java 21** or later; the server image ships its own JVM.

The full texts are in the repository: [LICENSE.txt](https://github.com/EventoFramework/evento-framework/blob/main/LICENSE.txt) (which module has which licence), [LICENSE-COMMERCIAL.txt](https://github.com/EventoFramework/evento-framework/blob/main/LICENSE-COMMERCIAL.txt). Contributions are accepted under the [Contributor License Agreement](https://github.com/EventoFramework/evento-framework/blob/main/CLA.md).
