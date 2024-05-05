# Domain Event

WIP

```java
package org.evento.common.modeling.messaging.payload;

public abstract class DomainEvent extends Event {
}

```

```java
package org.evento.demo.api.event;
import org.evento.common.modeling.messaging.payload.DomainEvent;

public class DemoCreatedEvent extends DomainEvent {

	private String demoId;
	private String name;
	private Long value;
	
	/** Getter, Setter, Constructors **/	
}

```
