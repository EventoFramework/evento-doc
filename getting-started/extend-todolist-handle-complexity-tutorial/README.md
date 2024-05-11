# Extend TodoList - Handle Complexity Tutorial

Congratulations! You've built a basic TodoList application. But what if you want to scale it up and ensure data integrity in a distributed environment? This chapter dives into advanced techniques to handle these complexities.

Here's what we'll explore:

* **Unique Identifier Generation with Sequence Consistency:** As your TodoList grows and potentially involves multiple servers, assigning unique identifiers to Todo items becomes crucial. We'll delve into strategies for generating guaranteed unique identifiers while maintaining sequence consistency. This ensures that identifiers are created in a specific order, even when requests are processed by different servers simultaneously.
* **Extensible Behaviors:** Learn to design your TodoList to accommodate future functionalities without compromising core functionality. We'll explore how Observers and Services can achieve this goal while maintaining Responsivity and Resilience.
* **Cross-Domain Consistency:** Imagine a scenario where completing a Todo triggers an update in another system, like an ERP service. We'll delve into the concept of eventual consistency and how Sagas can help achieve consistency across different domains. We'll also discuss the concept of "inconsistent by design."
* **Real-Time Data with MQTT:** Want to see your Todo list updates reflected instantly across devices? We'll explore how to integrate a real-time data provider like MQTT while considering its implications for eventual consistency within your TodoList application.

By the end of this chapter, you'll have a solid understanding of how to design and build robust TodoList applications that can scale and handle real-world complexities.
