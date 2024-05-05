# Domain Command

```java
package org.evento.common.modeling.messaging.payload;

public abstract class DomainCommand extends Command {
    public abstract String getAggregateId();
}

```

```java
package org.evento.demo.api.command;
import org.evento.common.modeling.messaging.payload.DomainCommand;

public class DemoCreateCommand extends DomainCommand {

	private String demoId;
	private String name;
	private Long value;

	/** Getter, Setter, Constructors **/

	@Override
	public String getAggregateId() {
		return demoId;
	}
}

```
