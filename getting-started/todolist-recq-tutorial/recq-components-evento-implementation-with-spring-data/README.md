# RECQ Components Evento Implementation with Spring Data

Now that we have implemented our payloads we can proceed with implementing components (Aggregates, Projector, Projections, Invokers) handling messages carrying those payloads.

{% hint style="info" %}
We suggest developing Aggregates and Services first, then Projector and Projections at the end Sagas or Observers. Invokers are the last.
{% endhint %}

We will proceed with this order:

* TodoListAggregate
* TodoList Domain in Spring Data
* TodoListProjector
* TodoListProjection
* TodoListInvoker
* Todo List Controller in Spring Web
