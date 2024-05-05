# Service Command

```java
package org.evento.common.modeling.messaging.payload;

public abstract class ServiceCommand extends Command {
	public String getLockId(){
		return null;
	}
}
```

```java
package org.evento.demo.api.command;

import org.evento.common.modeling.messaging.payload.ServiceCommand;

public class NotificationSendCommand extends ServiceCommand {
	private String body;
	
	/** Getter, Setter, Constructors **/
	
}
```
