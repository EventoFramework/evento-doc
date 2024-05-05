---
description: What is RECQ?
---

# Introduction

RECQ (Reactive, Event-Driven Commands and Queries) is a set of principles and patterns architectural, methodological, behavioural, and structural aimed at the creation of systems software with event-oriented microservices architectures compliant with the [Reactive Manifesto](https://www.reactivemanifesto.org/) and the more recent [Reactive Principles](https://www.reactiveprinciples.org/).

Another objective of the proposed methodology is to comply with the following rules, guidelines guides and patterns:&#x20;

* Avoid [Big Ball of Mud ](http://www.laputan.org/mud/)(Foote & Yoder, 1997)
* [Command-Query Separation](https://martinfowler.com/bliki/CommandQuerySeparation.html) (Fowler, CommandQuerySeparation, 2005)&#x20;
* [Separation of Concerns](https://en.wikipedia.org/wiki/Separation\_of\_concerns) (Dijkstra, 1982)&#x20;
* [Single Source of Truth](https://en.wikipedia.org/wiki/Single\_source\_of\_truth) (Pang & Szafron, 2014)&#x20;
* [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) (Martin, PrinciplesOfOod, 2005)&#x20;
* [Uniform Access Principle](https://en.wikipedia.org/wiki/Uniform\_access\_principle) (Meyer, 1997)&#x20;
* [Event Sourcing](https://microservices.io/patterns/data/event-sourcing.html)
* [Messaging](https://microservices.io/patterns/communication-style/messaging.html)&#x20;
* [Domain-Driven Design](https://it.wikipedia.org/wiki/Domain-driven\_design)

There are three Patterns:

* [RECQ System Pattern ](recq-system-pattern/)– an architectural pattern that defines high-level modules that make up a RECQ system.&#x20;
* [RECQ Communication Pattern](recq-communication-pattern/) – a behavioural pattern that defines how the elements communicate with each other.&#x20;
* [RECQ Component Patten](recq-system-pattern/component.md) – rigorously defining methodological aspects and individual responsibilities of each component of a RECQ system.
