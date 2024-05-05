---
description: >-
  A Component is a computational unit that implements the logic of the system,
  defined as actions.
---

# Component

### Properties

A component must submit to the following principles:&#x20;

* [Isolation ](https://www.reactivemanifesto.org/glossary#Isolation)– i.e. it is decoupled from each other, both from a temporal point of view and a spatial one. Therefore it does not have to make assumptions about the presence of other components e not even on their position in the system (Location Transparency).&#x20;
* Containment – in case a component needs to implement cross-resource logic these logics must be contained in the component same. Often this concept is also described as aggregation above all regarding Domain Driven Design: if a particular concept is strongly 33 coupled with another one creates an aggregate or a more complex domain than them contains both.&#x20;
* [Delegation ](https://www.reactivemanifesto.org/glossary#Delegation)– unlike the containment property, the concept of delegation forces us to limit the component to a minimal set of responsibilities. All that not is the direct responsibility of the component and must be delegated externally.

### Capabilities

A component can implement application logic only by exploiting the capabilities listed below:&#x20;

* It can receive messages dedicated to him and reply with a message to the sender – this capability allows the component to implement the concept of action since they depend on an external request. receiving a message, therefore, it corresponds to application logic.&#x20;
* Can have a persistent internal state, also called a local state.&#x20;
* Can publish System State Change Events.&#x20;
* Can consume System State Change Events.
* Can send messages to other components.&#x20;
* t must be replicable – therefore even in the presence of infinite instances of this component active in the system at the same time, no problems should arise.
