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

{% hint style="info" %}
**Changed in Evento v2.** The Spawn Instance / Kill Instance actions were removed. Evento Server no longer starts or stops bundle processes — that is owned by your orchestrator (e.g. Kubernetes or Nomad). This page is now a read-only view of the instances currently connected to the cluster.
{% endhint %}

By monitoring the Bundle Instances section, you can see which bundle instances are currently connected and confirm your cluster has the capacity it needs to handle the workload.

<figure><img src="../.gitbook/assets/image (65).png" alt=""><figcaption><p>Bundle Instances</p></figcaption></figure>

#### Consumers

The Consumers section provides a list of all active consumers within your cluster. For each consumer, the following information is displayed:

* **Consumer Name (Identifier):** The Consumer Identifier composed by the \{{Component Name\}} - \{{Component Version\}} (\{{Context\}})
* **Bundle**
* **Shared Instances:** A list of bundle instances with which the consumer is shared.

<figure><img src="../.gitbook/assets/image (66).png" alt=""><figcaption></figcaption></figure>

**By clicking on a specific consumer, you can access additional details, such as:**

* **Last Consumed Event Identifier:** The identifier of the last event processed by the consumer.
* **Dead Event Queue:** A list of events that failed to be processed. From here you can re-enqueue events for reprocessing or delete them — this is the only mutating action left in the GUI's otherwise read-only surface.

<figure><img src="../.gitbook/assets/image (67).png" alt=""><figcaption><p>Consumer Detailed Status</p></figcaption></figure>

The Cluster Status page, with its Bundle Instances and Consumers sections, offers a valuable tool for managing and monitoring your Evento cluster. By effectively utilizing this information, you can optimize performance, troubleshoot issues, and ensure the overall health of your system.

{% hint style="info" %}
Consumers register (and re-register) automatically every time a bundle establishes a session with the server. If the list is empty, make sure both the server and the bundles run Evento **2.3.1 or later** — earlier 2.x servers silently dropped consumer registrations.
{% endhint %}
