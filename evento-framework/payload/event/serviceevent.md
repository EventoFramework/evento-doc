# ServiceEvent

WIP

```java
package org.evento.common.modeling.messaging.payload;

public abstract class ServiceEvent extends Event {
}
```

```java
package org.evento.demo.api.event;
import org.evento.common.modeling.messaging.payload.ServiceEvent;

public class NotificationSentEvent extends ServiceEvent {
	private String notificationId;
	private String body;
	
	/** Getter, Setter, Constructors **/	
}
```
