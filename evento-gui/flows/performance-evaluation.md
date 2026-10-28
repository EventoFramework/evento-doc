---
description: Optimizing Your Evento Application
---

# Performance Evaluation

The Evento framework empowers you to not only build distributed applications but also to optimize their performance for efficiency and scalability. The performance evaluation feature, seamlessly integrated with Flows, provides valuable insights into how your application executes. By analyzing execution times, invocation frequencies, and flow structure, Evento helps you identify bottlenecks and understand the scalability properties of your system.

<figure><img src="../../.gitbook/assets/image (59).png" alt=""><figcaption></figcaption></figure>

#### Demystifying Performance Evaluation: A Collaborative Effort

The performance evaluation feature leverages a powerful combination of data sources to create an accurate picture of your application's performance:

* **Telemetry Data:** The Evento server persistently collects telemetry data about the execution time of handlers (components that process commands or events) and the invocation frequencies of these handlers within Flows. This data provides a real-world understanding of how long it takes for specific actions to occur and how often they are triggered.
* **Flow Structure:** The flow structure, as defined within your Evento application, outlines the sequence of interactions between components. This structure serves as a roadmap, allowing Evento to understand the interconnected nature of these interactions and how they contribute to the overall processing flow.

By analyzing this combined data, Evento builds a performance evaluation model. This model acts as a virtual representation of your application's performance characteristics.

#### How the model weighs each step

The model is an open queueing network: each handler, the server's gateway and the event store are stations, and each arrow carries the mean number of visits to its target per visit to its source.

* **Commands and queries a handler sends:** how many of each it sends per execution, measured.
* **Events a command produces (3.0.1):** one arrow per event the handler declares (its return type, or every class in `produces` for a handler that returns `DomainEvents`), weighted by how many events of that type one command produces on average, measured from every execution, zeros included. Below 1 for an event produced only sometimes (a service that may answer without an event, a discount applied to some orders), above 1 for one produced several times (one reservation per item). Until there are measurements the weight is 1.
* **The page labels** a weight up to 1 as a percentage and a weight above 1 as a multiplier (`× 3.00 per request`). The throughput an arrow carries is the source's throughput times its weight, so a consumer that receives three events per command receives three times the command rate, and the analysis can show it as the bottleneck.

Before 3.0.1 every command was modelled as producing exactly one event, its return type, every time.

#### Optimizing Throughput: Throughput Settings and Bottleneck Detection

The performance evaluation page within the Evento GUI offers functionalities to leverage the power of the performance evaluation model:

* **Throughput Settings:** You can specify the desired throughput (number of requests processed per unit time) for each Flow within your application. This allows you to define performance targets and identify Flows that might become bottlenecks if the workload increases.
* **Bottleneck Detection:** Based on the performance evaluation model, Evento can detect potential bottlenecks within your application. Bottlenecks are components or sections of Flows that become overloaded when the workload increases, hindering the overall performance. By identifying these bottlenecks, you can prioritize optimization efforts and ensure your application scales effectively.

#### Beyond the Page: Performance Optimization Strategies

The performance evaluation feature empowers you to make informed decisions about optimizing your Evento application. Here are some strategies you can employ:

* **Horizontal Scaling:** By increasing the number of bundle instances, you can distribute the workload across more resources, potentially alleviating bottlenecks.
* **Component Optimization:** If a specific component is identified as a bottleneck, you might explore techniques like code optimization or caching to improve its performance.
* **Flow Redesign:** In some cases, redesigning the flow structure itself might be necessary to optimize the sequence of interactions and reduce processing overhead.

#### Conclusion: A Guide to a Performant Evento Application

The performance evaluation feature, working hand-in-hand with Flows, serves as a powerful tool for optimizing your Evento application. By leveraging telemetry data, flow structure, and performance evaluation models, you gain valuable insights into your application's performance characteristics. This knowledge empowers you to identify bottlenecks, set throughput targets, and make informed decisions that ensure your application scales effectively to meet growing demands. As your Evento application evolves, the performance evaluation feature will remain your trusted companion, guiding you towards a performant and optimized system.
