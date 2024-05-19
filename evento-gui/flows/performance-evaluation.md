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
