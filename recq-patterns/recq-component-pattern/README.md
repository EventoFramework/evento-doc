---
description: Behavioral pattern that defines seven types of components.
---

# RECQ Component Pattern

This is a set of definitions with distinct and minimal semantics to implement any application, where minimality is not rigorous, but empirical deriving from the fact that most use cases can be designed with only the components described below.

<figure><img src="../../.gitbook/assets/image (21).png" alt=""><figcaption><p>RECQ Components Big Picture</p></figcaption></figure>

### Capability Table

In the following sections, the types will be defined, for each of which will be summarized capacity and scalability properties according to the [CAP theorem ](https://en.wikipedia.org/wiki/CAP\_theorem)using a defined table such as the "Capability Table", of which there is a generic version in Table 1. The first five entries refer to message handlers they can react to and the invocations they can make. By type of state we mean if a handler to be executed requires, in addition to the input message, also a state of some sort kept consistent by component;&#x20;

There are two types of status:

* **Instance**: A type of state that is based on a single instance of a domain object or a particular resource. So there can be multiple Handlers at the same time running in this component as long as they are handling resource requests or different objects.
* **Component**: There can be no more than one handler for this particular component active that handles a request.

The last entry refers to the properties of the CAP theorem respected by the component:

* C: component implements strong consistency, it happens in components that have a state that must be kept consistent regardless of the type of message handled.&#x20;
* c: the component implements weak consistency, so the consistency is only in managed message function.&#x20;
* A: The component implements strong availability, and the response time is known a priori.&#x20;
* a: the component implements weak availability, the response time is known a priori provided that the requests do not refer to the same resource.&#x20;
* P: partitioning tolerance, being a distributed system this constraint must always be present.

| Capability                  |                       |
| --------------------------- | --------------------- |
| Can handle Command Messages | Yes/No                |
| Can handle Query Messages   | Yes/No                |
| Can handle Events           | Yes/No                |
| Can send Command Messages   | Yes/No                |
| Can Send Query Messages     | Yes/No                |
| State type                  | Instance/Component/No |
| CAP Properties              | C/c/A/a/P             |
