---
description: Building Microservices with Evento Framework - Beyond RECQ with @Component
---

# @Component

Welcome to the world of building robust microservices with the Evento Framework! This chapter dives into the heart of Evento - the `@Component` module. Here, you'll discover how it empowers you to seamlessly map your meticulously designed RECQ Architecture directly into clean and maintainable Java code.

The RECQ Architecture provides a blueprint for structuring microservices based on four key building blocks:

* **Events:** Capture actions or state changes that occur within your domain. These are immutable data objects representing a specific event that has happened.
* **Commands:** Initiate actions that modify the state of your domain. They represent instructions to be carried out by the system.
* **Queries:** Retrieve information about your domain without altering its state. They are used to fetch data for display or further processing.

The `@Component` module bridges the gap between your RECQ architecture and its Java implementation. It provides a set of annotations that map these components to their corresponding Java classes:

* **Aggregate (@Aggregate):** Used with `@Aggregate` to define an Aggregate Root, a cluster of related entities treated as a single unit of consistency.
* **Service (@Service):** Leverages `@Service` to create reusable business logic components, promoting code organization.
* **Projector and Projection (@Projector, @Projection):** Employs `@Projection` to build materialized views based on events, allowing efficient data retrieval for specific needs.
* **Saga (@Saga):** Utilizes `@Saga` to define long-running transactions that might span multiple services, ensuring data consistency across your architecture.
* **Observer (@Observer):** The `@Observer` annotation enables implementing the Observer pattern, allowing components to react to specific events loosely.
* **Invoker (@Invoker):** Separates command and query handling using `@Invoker`. This promotes loose coupling within your architecture.

By combining these annotations with the core RECQ components, you can create robust and adaptable microservices. The `@Component` module ensures a consistent approach to defining and managing these components, leading to clean and maintainable code.

In the following chapters, we'll delve deeper into each RECQ component and explore the extended functionalities provided by the `@Component` module. Each chapter will focus on a specific annotation, providing detailed explanations, code examples, and best practices for its application.

This chapter structure allows you to gain a comprehensive understanding of the `@Component` module and its role in implementing the RECQ Architecture in your Evento microservices. So, buckle up and get ready to unlock the full potential of clean and maintainable code for building exceptional microservices!
