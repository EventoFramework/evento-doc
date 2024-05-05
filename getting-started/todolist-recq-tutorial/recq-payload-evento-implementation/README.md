# RECQ Payload Evento Implementation

Once we've defined all our payloads or "message types" we need to implement them using Evento Framework creating a Class for each Payload and adding required fields to handle those messages properly.

* Domain Command
* Domain Events
* Queries
* Views

{% hint style="info" %}
As a best practice, we suggest storing all Payloads inside a common library inside a package called "API" like: `com.eventoframework.demo.todo.api`

Then device payloads by domain and then by type following this sample scaffolding:

```
├───user
│   ├───command
│   ├───event
│   ├───query
│   ├───view
│   └───enum
└───todo
    ├───command
    ├───event
    ├───query
    ├───view
    └───enum
```
{% endhint %}

