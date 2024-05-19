---
description: A Comprehensive View of Your RECQ System
---

# Application Graph

Within the intricate world of RECQ architectures, visualizing the interplay between components and their interactions is paramount. Evento, a framework designed for building RECQ applications, offers the Application Graph – a powerful graphical representation that unveils the structure and organization of your entire system. Unlike traditional flow diagrams that depict a predefined sequence, the Application Graph utilizes a nested circle structure to comprehensively portray the hierarchical relationships between bundles, components, and handlers.

<figure><img src="../.gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>

#### Decoding the Nested Circles: A Hierarchical View

The Application Graph leverages a unique visual approach to represent the building blocks of your RECQ application:

* **Outermost Circles:** These circles represent the **bundles** within your system. Bundles encapsulate a collection of components that work together to deliver specific functionalities. Their placement on the outermost layer signifies their top-level position within the application hierarchy.
* **Mid-Level Circles:** Nested within the bundle circles are circles representing the **components**. These are the workhorses of your application, responsible for handling specific tasks such as processing commands, generating events, or querying data. Their placement within their corresponding bundle circle reflects their belonging to that particular functional unit.
* **Innermost Circles:** At the core of the component circles, you might find even smaller circles representing **handlers**. Handlers are the most granular units of execution within a component. They define how a component reacts to specific events or commands. Their placement within the component circle reflects their role as specific functionalities within that component.

This nested structure offers a clear visual hierarchy, allowing you to grasp the relationships between these elements at a glance.

#### Unveiling the Connections: Beyond the Hierarchy

While the nested circles represent the application's structure, the magic of the Application Graph lies in the connections it reveals:

* **Lines Between Bundles:** Lines connecting bundle circles might indicate dependencies between bundles. These dependencies showcase how bundles rely on functionalities provided by other bundles to achieve their goals.
* **Lines Between Components:** Lines connecting component circles within a bundle represent interactions between components. These interactions might involve one component publishing events that another component subscribes to, or one component invoking services provided by another.

By analyzing these connections, you gain insights into how data flows and events are orchestrated throughout your application.

#### Exploring the Application Graph: A Gateway to Deeper Understanding

The Evento GUI allows you to interact with the Application Graph, providing further details about each element:

* **Hovering Over Elements:** Hovering over a circle might reveal a tooltip with additional information, such as the name of the bundle, component, or handler.
* **Clicking on Elements:** Clicking on a circle might navigate you to a dedicated page with detailed information about the selected element. For bundles, you might see a list of their components. For components, you might see a description of their purpose and the handlers they contain.

This interactive exploration empowers you to delve deeper into the intricate workings of your RECQ application.

#### Beyond the Application Graph: Understanding the Bigger Picture

The Application Graph serves as a valuable tool for understanding the overall structure and organization of your RECQ system. However, remember that a holistic understanding requires considering additional aspects:

* **Flows:** Flows represent the specific execution paths taken within your application. They define the sequence of interactions between components triggered by a particular event or command. While the Application Graph offers a static view, Flows provide a dynamic perspective on how these interactions unfold.

In conclusion, the Application Graph, working in conjunction with Flows, offers a comprehensive understanding of your Evento application. By leveraging the hierarchical structure, connections between elements, and interactive exploration features, you gain valuable insights into how bundles, components, and handlers collaborate to deliver the functionalities of your RECQ system. As your application evolves, the Application Graph will remain a trusted visual reference, aiding you in understanding its architecture and guiding you towards informed development decisions.
