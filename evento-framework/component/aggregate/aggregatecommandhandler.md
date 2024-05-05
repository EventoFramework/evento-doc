# @AggregateCommandHandler

```java
package org.evento.common.modeling.annotations.handler;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD})
@Handler
public @interface AggregateCommandHandler {
    boolean init() default false;
}
```

<pre class="language-java"><code class="lang-java">import org.evento.common.modeling.annotations.handler.AggregateCommandHandler;
<strong>// ...
</strong><strong>
</strong><strong>@AggregateCommandHandler(init = true)
</strong>DemoCreatedEvent handle(DemoCreateCommand command,
			DemoAggregateState state,
			CommandGateway commandGateway,
			CommandMessage&#x3C;DemoCreateCommand> commandMessage) {
	Utils.doWork(1200);
	return new DemoCreatedEvent(
			command.getDemoId(),
			command.getName(),
			command.getValue());
}

@AggregateCommandHandler
DemoUpdatedEvent handle(DemoUpdateCommand command,
			DemoAggregateState state) {
	if (state.getValue() >= command.getValue()) // Validation Step
		throw new RuntimeException("error.invalid.value");
	Utils.doWork(1100); // Work Step
	return new DemoUpdatedEvent(
			command.getDemoId(),
			command.getName(),
			command.getValue());
}
</code></pre>
