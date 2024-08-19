---
description: >-
  The Cluster Status page provides a comprehensive overview of the health and
  status of your Evento cluster. It consists of two primary sections: Bundle
  Instances and Consumers.
---

# Cluster Status (Experimental)

#### Bundle Instances

The Bundle Instances section displays all connected bundles within your cluster. Each bundle is represented by a card containing essential information:

* **Bundle Name:** The unique identifier of the bundle.
* **Status:** The current status of the bundle (e.g., Available, Unavailable).
* **Replica Count:** The number of instances running for the bundle.
* **Instance IDs:** A list of the unique identifiers for each bundle instance.

**Actions:**

You can perform the following actions on bundle instances:

* **Spawn Instance:** Create a new instance of the bundle to increase its capacity or redundancy.
* **Kill Instance:** Terminate an existing instance of the bundle.

By monitoring the Bundle Instances section, you can ensure that your cluster has the necessary resources to handle the workload and maintain optimal performance.

<figure><img src="../.gitbook/assets/image (65).png" alt=""><figcaption><p>Bundle Instances</p></figcaption></figure>

#### Consumers

The Consumers section provides a list of all active consumers within your cluster. For each consumer, the following information is displayed:

* **Consumer Name (Identifier):** The Consumer Identifier composed by the \{{Component Name\}} - \{{Component Version\}} (\{{Context\}})
* **Bundle**
* **Shared Instances:** A list of bundle instances with which the consumer is shared.

<figure><img src="../.gitbook/assets/image (66).png" alt=""><figcaption></figcaption></figure>

**By clicking on a specific consumer, you can access additional details, such as:**

* **Last Consumed Event Identifier:** The identifier of the last event processed by the consumer.
* **Dead Event Queue:** A list of events that failed to be processed, allowing for manual reprocessing.

<figure><img src="../.gitbook/assets/image (67).png" alt=""><figcaption><p>COnsumer Detailed Status</p></figcaption></figure>

The Cluster Status page, with its Bundle Instances and Consumers sections, offers a valuable tool for managing and monitoring your Evento cluster. By effectively utilizing this information, you can optimize performance, troubleshoot issues, and ensure the overall health of your system.

**Note:** Based on the provided information, the Consumers section appears to be under development, and the full functionality may not be available in the current version of the interface.
