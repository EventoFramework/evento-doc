# Payload Catalog

Within the intricate world of Evento applications built on the Evento framework, payloads act as the fundamental building blocks of communication. These payloads carry valuable data exchanged between components, orchestrating actions and driving the system's behavior. The Evento GUI's Payload Catalog serves as a comprehensive map, guiding you through the landscape of all registered payloads within your distributed system.

#### A Centralized Repository: Unveiling the Payload Landscape

<figure><img src="../.gitbook/assets/image (53).png" alt=""><figcaption><p>List of all Payloads</p></figcaption></figure>

The Payload Catalog offers a centralized location to explore and understand the diverse set of payloads utilized by your Evento application. Here's what you'll encounter on this valuable page:

* **Comprehensive Payload List:** The central section of the Payload Catalog showcases a meticulously organized table. This table serves as your primary tool for navigating the plethora of payloads available.
  * **Search Functionality:** A search bar positioned above the table empowers you to filter the list based on keywords or specific criteria. This functionality allows you to quickly locate payloads of interest, especially within large-scale applications.
  * **Payload Overview:** Each row in the table represents a single payload within your system. Key attributes of each payload are likely displayed within dedicated columns, offering a concise overview:
    * **Name:** This column displays a unique identifier or name assigned to each payload, allowing for easy recognition.
    * **Type:** This column categorizes the payloads based on their purpose within your application. Examples might include "Query," "DomainCommand," "DomainEvent," "View," "ServiceEvent," or "ServiceCommand." Understanding the type provides insight into how the payload interacts with other components.
    * **Invocations** (or **Producers**): This column might indicate the number of times a particular payload is invoked or the number of components that generate it. This metric helps gauge how frequently a payload is used within the system.
    * **Component:** This column might identify the specific component within a bundle that is responsible for generating or handling the payload. This information fosters understanding of how components interact and collaborate.

**Refining Your Exploration: Filter Panels for Focused Discovery**

The Payload Catalog doesn't stop at simply presenting the entire list. Recognizing the potential vastness of payloads in complex systems, the GUI offers additional functionalities to refine your exploration:

* **Filter by Type:** This filter panel allows you to narrow down the displayed payloads based on their specific type. By selecting a particular type (e.g., "Query"), you can focus on payloads that serve a specific purpose within your application.
* **Filter by Domain:** This filter panel fosters exploration based on the domain or functional area of your application. Selecting a specific domain (if available) displays only payloads relevant to that section, aiding in understanding data flow within that domain.
* **Filter by Component:** This filter panel empowers you to concentrate on payloads associated with a particular component. Selecting a component displays only payloads that it generates or handles, providing a targeted view of that component's role in the system.

By skillfully utilizing the search bar and filter panels in conjunction with the provided payload details, you can efficiently navigate and explore the vast repository of payloads within your Evento application.

#### Beyond the List: Unveiling Payload Interactions

<figure><img src="../.gitbook/assets/image (55).png" alt=""><figcaption><p>Domain Command Payload Detailed View</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (56).png" alt=""><figcaption><p>Domain Event Payload Detailed View</p></figcaption></figure>

The Payload Catalog doesn't merely present a static list. Clicking on a specific payload within the table unlocks a new level of detail. This detailed payload view delves deeper, revealing:

* **Comprehensive Payload Description:** This section provides a more in-depth explanation of the payload's purpose and functionality within the system. It might also include details about the data structure it carries.
* **Component Interactions:** This section sheds light on how the chosen payload interacts with other components within your application. Visual representations or textual descriptions might illustrate the producer-consumer relationships between the payload and various components. This fosters understanding of how data flows through the system and how different parts collaborate.
* **Related Payloads:** This section might showcase other payloads that are directly linked to the selected one. These might be payloads generated as a response to a query, or payloads that trigger a specific event. Understanding these relationships paints a clearer picture of the overall data flow and event processing within your application.

By delving into the detailed payload view, you gain a deeper understanding of how each payload plays its role in the grand orchestration of your Evento application.

#### Conclusion: The Payload Catalog - A Gateway to Understanding

The Payload Catalog serves as an invaluable asset within the Evento GUI. By offering a comprehensive view of registered payloads, coupled with search, filter, and detail exploration functionalities, the Catalog empowers you to navigate the intricate data flow within your distributed system. As you delve deeper into your Evento application, the Payload Catalog will remain your trusted companion, aiding in understanding overall system behavior and optimizing communication between components.
