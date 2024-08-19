# Payload and Messages

In Evento Framework, **Messages** and **Payloads** are the workhorses of communication within your event-driven architecture. They work together to ensure data flows effectively between components:

**Messages:**

* Imagine envelopes carrying instructions and relevant data. Messages in Evento act similarly. They encapsulate the following:
  * **Payload:** The core data carrier, holding information specific to the message type (Event, Command, View, or Query).
  * **Message Type:** An indicator specifying the type of message (e.g., "OrderCreatedEvent", "UpdateCustomerCommand").
  * (Optional) **Routing Details:** Additional information used for routing the message to the appropriate handler within the receiving component.

**Here's an analogy:**

Think of a restaurant order. The order itself (**Message**) specifies what's being requested (**message type**). The specific dishes (**payload**) detail the order contents. Routing details might include table number or a specific chef for a specialized dish.

**Payloads:**

* These are the data carriers residing within messages. They represent the specific information associated with the message type:
  * **Event Payloads:** Carry data about events that have occurred within the system (e.g., "OrderCreatedEvent" payload might include details like order ID, items ordered, etc.).
  * **Command Payloads:** Encapsulate data required to perform actions (e.g., "UpdateCustomerCommand" payload might include new customer information).
  * **View Payloads:** Hold data requested by views to construct a specific representation (e.g., "CustomerDetailsView" payload might include customer name, address, etc.).
  * **Query Payloads:** Carry data retrieved in response to queries (e.g., "GetOrderByIdQuery" payload might include order details based on the provided ID).

**Key Points:**

* **Flexibility:** Payloads can have different structures depending on the message type. They can range from simple data types to complex objects representing domain concepts.
* **Data-Centric:** Payloads primarily focus on data representation. They don't contain any logic or functionality themselves. The receiving component interprets the data within the payload to perform the desired action or fulfill the request.
* **Serialization:** Evento Framework might utilize serialization mechanisms (like converting payloads to a byte stream) for efficient storage or transmission within messages.

**Understanding Messages and Payloads is Crucial:**

By grasping how Messages and Payloads work together, you can effectively design and implement communication channels within your event-driven applications built with Evento Framework. Messages ensure structured communication, while Payloads carry the essential data that drives actions and information retrieval.

### Message in Evento Framework

```java
package com.evento.common.modeling.messaging.message.application;

import com.evento.common.modeling.messaging.payload.Payload;
import com.evento.common.modeling.messaging.payload.TrackablePayload;
import com.fasterxml.jackson.annotation.JsonIgnore;

import java.io.Serializable;
import java.time.Instant;

/**
 * The Message class is an abstract class that represents a message.
 * It contains a serialized payload, timestamp, and metadata.
 * Messages can be subclassed for specific types of messages.
 *
 * @param <T> The type of the payload.
 */
public abstract class Message<T extends Payload> implements Serializable {

	private SerializedPayload<T> serializedPayload;

	private long timestamp;

	private Metadata metadata;

	private boolean forceTelemetry = false;

	/**
	 * Constructs a new Message object with the given payload.
	 *
	 * @param payload The payload of the Message.
     */
	public Message(T payload) {
		this.serializedPayload = new SerializedPayload<>(payload);
		this.timestamp = Instant.now().toEpochMilli();
		if(payload instanceof TrackablePayload pc){
			setForceTelemetry(pc.isForceTelemetry());
		}
	}

	/**
	 * The Message class represents a message with a serialized payload, timestamp, and metadata.
	 *
     */
	public Message() {
	}

	/**
	 * Retrieves the payload of the message.
	 *
	 * @return the payload of the message
	 */
	@JsonIgnore
	public T getPayload() {
		return serializedPayload.getObject();
	}

	/**
	 * Sets the payload of the message.
	 *
	 * @param payload The payload to be set.
     */
	public void setPayload(T payload) {
		this.serializedPayload = new SerializedPayload<>(payload);
	}

	/**
	 * Retrieves the serialized payload of the message.
	 *
	 * @return the serialized payload of the message
	 */
	public SerializedPayload<T> getSerializedPayload() {
		return serializedPayload;
	}

	/**
	 * Sets the serialized payload of the Message.
	 *
	 * @param serializedPayload The serialized payload to be set.
     */
	public void setSerializedPayload(SerializedPayload<T> serializedPayload) {
		this.serializedPayload = serializedPayload;
	}

	/**
	 * Retrieves the metadata of the message.
	 *
	 * @return The metadata object associated with the message.
	 */
	public Metadata getMetadata() {
		return metadata;
	}

	/**
	 * Sets the metadata of the message.
	 *
	 * @param metadata The metadata to be set.
	 */
	public void setMetadata(Metadata metadata) {
		this.metadata = metadata;
	}

	/**
	 * Retrieves the type of the message.
	 *
	 * @return the type of the message as a String.
	 */
	public String getType() {
		return serializedPayload.getObjectClass();
	}

	/**
	 * Retrieves the name of the payload.
	 *
	 * @return the name of the payload as a String.
	 */
	public String getPayloadName() {
		var parts = getType().split("\\.");
		return parts[parts.length - 1];
	}

	/**
	 * Retrieves the timestamp of the message.
	 *
	 * @return The timestamp of the message.
	 */
	public long getTimestamp() {
		return timestamp;
	}

	/**
	 * Sets the timestamp of the message.
	 *
	 * @param timestamp The timestamp to be set.
	 */
	public void setTimestamp(long timestamp) {
		this.timestamp = timestamp;
	}

	/**
	 * Retrieves the value indicating whether force telemetry is enabled for the message.
	 *
	 * @return True if force telemetry is enabled, False otherwise.
	 */
	public boolean isForceTelemetry() {
		return forceTelemetry;
	}

	/**
	 * Sets the value indicating whether force telemetry is enabled for the message.
	 *
	 * @param forceTelemetry True to enable force telemetry, False to disable it.
	 */
	public void setForceTelemetry(boolean forceTelemetry) {
		this.forceTelemetry = forceTelemetry;
	}
}

```

**Methods:**

* **Constructor:**
  * `public Message(T payload)`: This constructor takes a payload object (`T` extending `Payload`) as an argument. It likely initializes the `serializedPayload` object with the provided payload and sets the timestamp using `Instant.now().toEpochMilli()`.
* **Getters and Setters:**
  * `public T getPayload()`: Retrieves the actual payload object (`T`) from the `serializedPayload` object. This likely involves deserialization if the payload was stored in a serialized format.
  * `public void setPayload(T payload)`: Sets the payload of the message by updating the `serializedPayload` object with the provided payload (`T`). This might involve serialization for storage or transmission.
  * `public SerializedPayload<T> getSerializedPayload()`: Returns the internal `SerializedPayload` object holding the serialized representation of the payload.
  * `public void setSerializedPayload(SerializedPayload<T> serializedPayload)`: Sets the internal `SerializedPayload` object with the provided serialized payload information.
* **Type and Payload Name Retrieval:**
  * `public String getType()`: Utilizes the `serializedPayload` object to determine the class name of the payload object (`T`). This provides a string representation of the message type.
  * `public String getPayloadName()`: Extracts the name of the payload class from the full type string retrieved by `getType()`. This isolates the actual payload class name (useful for identifying the specific payload structure).
* **Timestamp:**
  * `public long getTimestamp()`: Returns the timestamp of the message, likely set during initialization using `Instant.now().toEpochMilli()`.
  * `public void setTimestamp(long timestamp)`: Allows setting a custom timestamp for the message, potentially for testing or specific use cases.
* **Metadata (Optional):**
  * The provided code snippet doesn't explicitly show methods for accessing or manipulating metadata. However, the `Message` class might have getter and setter methods for a `Metadata` object (not provided) to attach and retrieve additional information associated with the message.
* **Force Telemetry (Optional):**
  * **Purpose:** By setting `forceTelemetry` to `true`, you explicitly instruct the [Evento framework to collect and store telemetry data](../../evento-gui/component-catalog.md#telemetry) for this particular message, regardless of the system's default telemetry settings. This can be useful for troubleshooting critical events or monitoring performance of specific message types.
  * **Default Behavior:** When `forceTelemetry` is `false` (the default setting), telemetry collection adheres to the overall system configuration for the message type.

**Key Points:**

* These methods provide access to the core elements of a message: payload, type information, timestamp, and potentially metadata.
* Getters and setters allow for retrieving and modifying the message structure as needed.
* Methods like `getType` and `getPayloadName` offer convenient ways to identify the type of message and the specific payload class it carries.

**Understanding these methods is essential for effectively working with messages in Evento Framework. They allow you to construct messages with the appropriate payload, access the carried data, and potentially manage additional information through metadata.**

