---
description: Everything public; Apache-2.0 client libraries, Apache-2.0 with the Commons Clause for the server
---

# Licensing

All of Evento is public, with every feature: the server, the web console with [single sign-on and the audit trail](evento-gui/gui-auth.md), the client libraries. There is no closed edition. Two licences apply.

| Component | Licence |
|---|---|
| Client libraries: `evento-bundle`, `evento-common`, `evento-transport-api`, `evento-transport-netty`, `evento-consumer-state-store-jdbc`, `evento-spring-boot-starter`, `evento-opentelemetry`, `evento-test` | **Apache-2.0** |
| Evento Server, the web console and everything else | **Apache-2.0 with the Commons Clause** |

* **Your application** depends only on the client libraries: no obligation on it, whatever its own licence, free or sold.
* **The server** you can use, change and run freely, in production, in any organisation, also to sell your own products built on it (an online shop, a SaaS product of your own): what you sell is your application, not Evento.
* **What needs a written authorisation** is selling Evento itself. The Commons Clause takes away the right to provide the software, or a service whose value derives substantially from it, to third parties for a fee: offering Evento as a hosted or managed service, reselling it or a fork of it, selling consulting, support or training about it. Ask at [eventoframework.com/licensing](https://www.eventoframework.com/licensing/).
* **The names Evento and RECQ** may be used to refer to the project, not in the name or the marketing of a commercial product or service without authorisation ([TRADEMARKS.md](https://github.com/EventoFramework/evento-framework/blob/main/TRADEMARKS.md)). The RECQ architecture itself is an idea: anyone may study it and apply it.

The Commons Clause makes the server source-available rather than open source in the sense of the Open Source Definition; the client libraries are not affected by it.

The client libraries run on **Java 21** or later; the server image ships its own JVM.

The full texts are in the repository: [LICENSE.txt](https://github.com/EventoFramework/evento-framework/blob/main/LICENSE.txt) (which module has which licence, and what is allowed), [LICENSE-COMMERCIAL.txt](https://github.com/EventoFramework/evento-framework/blob/main/LICENSE-COMMERCIAL.txt) (the authorisation agreement), [TRADEMARKS.md](https://github.com/EventoFramework/evento-framework/blob/main/TRADEMARKS.md). Contributions are accepted under the [Contributor License Agreement](https://github.com/EventoFramework/evento-framework/blob/main/CLA.md).
