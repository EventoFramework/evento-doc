---
description: Understanding Event Payloads and Event Messages in Evento Framework
---

# Event

Event-driven architectures rely heavily on the exchange of messages carrying event information. In Evento Framework, two key concepts play a crucial role in this communication: Event Payloads and Event Messages. This chapter dives into their functionalities and how they work together to facilitate efficient event handling within your system.

#### Event Payload: The Core of the Event

An Event Payload represents the heart of an event within Evento Framework. It's a structured object that encapsulates the specific data associated with an event occurrence. Here's what defines an Event Payload:

* **Foundation:** It extends the base `Payload` class, likely inheriting functionalities for serialization and deserialization, allowing the payload to be efficiently transmitted and stored within the system.
* **Abstract Base Class:** The `Event` class acts as an abstract base class for all event payloads. It defines common functionalities like context management (discussed later) and serves as a foundation for concrete event classes.
* **Concrete Event Classes:** You wouldn't directly use the `Event` class itself. Instead, you define concrete event classes that inherit from `Event`. These classes represent specific events within your domain or service logic.
* **Event-Specific Data:** Each concrete event class adds its own data members and potentially behavior specific to the event it represents. For example, an `OrderCreatedEvent` payload might contain information about the ordered products, customer details, and order total.

**Benefits of Event Payloads:**

* **Structured Data:** Event payloads enforce a structured approach to representing event data, improving maintainability and clarity.
* **Type Safety:** Inheritance from `Event` ensures type safety and consistency when working with different event types.
* **Flexibility:** Concrete event classes allow for customization based on the specific information each event needs to convey.

#### Event Implementation

```java
package com.evento.common.modeling.messaging.payload;

import com.evento.common.utils.Context;

/**
 * The Event class represents an abstract base class for events in a software system.
 * It extends the Payload class.
 *
 * @see Payload
 */
public abstract class Event implements Payload {
    private String context = Context.DEFAULT;

    /**
     * Returns the context of the event.
     * <p>
     * The context is a string value representing the available context options for certain functionalities within a software system.
     * It is set by calling the setContext method.
     * The context can be accessed using the getContext method.
     *
     * @return the context of the event as a string
     *
     * @see #setContext(String)
     * @see Event#setContext(String)
     */
    public String getContext() {
        return context;
    }

    /**
     * Sets the context of the event.
     * The context is a string value representing the available context options for certain functionalities within a software system.
     * It is set by calling the setContext method.
     *
     * @param context the context to be set as a string
     * @throws IllegalArgumentException if the context provided is null
     * @return the updated event object with the new context
     *
     * @see Event#getContext()
     * @param <T> the event
     */
    @SuppressWarnings("unchecked")
    public <T extends Event> T setContext(String context) {
        if(context ==  null){
            throw new IllegalArgumentException();
        }
        this.context = context;
        return (T) this;
    }
}
```

* The `Event` class acts as the foundation for all event payloads. It's an abstract class meaning you wouldn't directly create instances of `Event` itself.
* It likely inherits from a base `Payload` class (not shown), which might provide functionalities for serialization and deserialization, allowing payloads to be efficiently transmitted and stored.
* `Event` offers methods for managing context:
  * `getContext()`: Retrieves the context string associated with the event (optional).
  * `setContext(String context)`: Sets the context string for the event (optional).

#### Context

The concept of Context within Evento Framework provides a way to categorize events based on a key, enabling parallel and consistent event consumption. This functionality is particularly useful when handling the same event type with different processing requirements depending on the context.

For instance, imagine a `UserCreatedEvent`. By default, these events might be processed in a generic way. However, with Contexts, you can differentiate user creations based on their region. You could set contexts like "EU" or "USA" on the event, allowing for parallel processing specifically tailored for each region. This approach ensures consistent handling within each context while enabling efficient parallel processing for different categories of the same event type. We'll delve deeper into how Contexts are utilized within the `@Component` annotation in a dedicated chapter.

#### Event Message: The Delivery Vehicle

An Event Message acts as a container or envelope for delivering an Event Payload within Evento Framework. It carries the payload along with additional information necessary for routing and processing the event. Here's a breakdown of its functionalities:

* **Message Class:** It extends the base `Message` class, likely inheriting functionalities for storing message metadata (timestamp, type information).
* **Payload Holder:** The core element of an Event Message is the payload itself, which is an instance of an `Event` subclass (DomainEvent, ServiceEvent, etc.).
* **Context (Optional):** Similar to Event Payloads, Event Messages can optionally store a context string. This context might be used for influencing processing or routing decisions for the message.
* **Event Message Creation:** You typically create Event Messages by providing the concrete Event object (payload) you want to send. Evento Framework likely offers functionalities for constructing and sending these messages.

**Benefits of Event Messages:**

* **Encapsulation:** Event Messages encapsulate the event payload along with necessary metadata, promoting a clean separation of concerns.
* **Routing Information:** Messages might contain routing information that allows the framework to direct the event to the appropriate handler for processing.
* **Contextual Awareness:** Optional context information can provide additional context for processing the event within the system.

#### Event Message Definition

```java
package com.evento.common.modeling.messaging.message.application;

import com.evento.common.modeling.messaging.payload.Event;
import com.evento.common.utils.Context;

/**
 * EventMessage is an abstract class that represents a message containing an event payload.
 *
 * @param <T> The type of the event payload.
 */
public abstract class EventMessage<T extends Event> extends Message<T> {

    private String context;
    /**
     * Constructs a new EventMessage with the given payload.
     *
     * @param payload the payload of the EventMessage
     *
     */
    public EventMessage(T payload) {
       super(payload);
       this.context = payload == null ? Context.DEFAULT : payload.getContext();
    }

    /**
     * EventMessage is a class that represents a message containing an event payload.
     *
     */
    public EventMessage() {
    }

    /**
     * Returns the name of the event.
     *
     * @return the name of the event
     */
    public String getEventName() {
       return getPayloadName();
    }

    /**
     * Retrieves the value of the association property from the serialized payload used by saga components.
     *
     * @param associationProperty the property key of the association
     * @return the value of the association property as a string
     */
    public String getAssociationValue(String associationProperty) {
       return getSerializedPayload().getTree().get(1).get(associationProperty).textValue();
    }

    /**
     * Retrieves the context of the EventMessage.
     * <p>
     * The context is a string value representing the available context options for certain functionalities within a software system.
     * It is set by calling the setContext method of the Event object.
     * The context can be accessed using the getContext method of the Event object.
     *
     * @return the context of the EventMessage as a string
     *
     * @see Event#setContext(String)
     * @see Event#getContext()
     * @see EventMessage#setContext(String)
     */
    public String getContext() {
       return context;
    }

    /**
     * Sets the context of the EventMessage.
     * <p>
     * The context is a string value representing the available context options for certain functionalities within a software system.
     * It is set by calling the setContext method of the Event object.
     *
     * @param context the context to be set as a string
     *
     * @see Event#setContext(String)
     * @see EventMessage#getContext()
     */
    public void setContext(String context) {
       this.context = context;
    }
}
```

**Functionality:**

* EventMessage acts as an abstract class representing a message specifically designed to carry an event payload within your event-driven architecture.
* It extends a base `Message` class (not shown), likely inheriting functionalities for storing message metadata (timestamp, type information) relevant for routing and processing.

**Key Features:**

* **Payload Specialization:** It enforces the payload type to be an `Event` object, ensuring messages specifically carry event information.
* **Context (Optional):** Similar to Event Payloads, Event Messages can optionally store a context string. This context might be used for influencing processing or routing decisions for the message.
* **Constructors:**
  * **Primary Constructor (`EventMessage(T payload)`):**
    * Takes an `Event` object (payload) and likely calls the superclass constructor (`Message`) to initialize the message metadata.
    * Sets the context property by either using the provided payload's context (if available) or a default context value.
  * **Empty Constructor (`EventMessage()`):**
    * Exists for potential subclassing or specific use cases where the payload might be set later.
* **Event Name Access:**
  * `getEventName()`: Delegates to the `getPayloadName()` method inherited from `Message`, effectively returning the name of the event class carried by the payload.
* **Association Value Retrieval (for Sagas):**
  * `getAssociationValue(String associationProperty)`: This method retrieves the value of an association property from the serialized payload. This functionality might be specifically used by saga components within the framework for handling long-running business processes that span multiple events.
* **Context Management:**
  * `getContext()`: Retrieves the context string associated with the Event Message.
  * `setContext(String context)`: Sets the context string for the Event Message.

**Overall:**

EventMessage provides a structured approach for creating messages that carry event payloads within Evento Framework. It leverages inheritance from the base `Message` class while adding functionalities specific to events, like context handling and potentially association value access for saga components.

#### Relationship Between Event Payloads and Event Messages

Event Payloads and Event Messages work together to deliver event information within Evento Framework. Here's how they interact:

1. **Concrete Event Creation:** You define concrete event classes (e.g., `OrderCreatedEvent`) that inherit from `Event` and contain the specific data for your event. These classes represent the event payload itself.
2. **Event Message Construction:** When you want to send an event, you create an Event Message object. This message likely involves providing the concrete event object (payload) you want to deliver.
3. **Delivery and Processing:** The Event Message, containing the event payload, is then sent through Evento Framework's mechanisms. The framework might handle routing and delivery to the appropriate handler based on the event type or other message metadata.
4. **Event Handling:** The event handler receives the Event Message and extracts the event payload (the concrete event object) for processing. The handler logic can access the event-specific data within the payload to perform the necessary actions based on the event type.

**In essence, Event Payloads represent the core data associated with an event, while Event Messages act as the delivery vehicle for sending that data within Evento Framework.** The combination of these concepts allows for efficient communication and handling of events throughout your event-driven application.
