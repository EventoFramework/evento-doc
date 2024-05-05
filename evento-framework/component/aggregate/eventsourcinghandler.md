# @EventSourcingHandler

```java
package org.evento.common.modeling.annotations.handler;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD})
@Handler
public @interface EventSourcingHandler {
}
```

<pre class="language-java"><code class="lang-java">import org.evento.common.modeling.annotations.handler.EventSourcingHandler;
//...

@EventSourcingHandler
DemoAggregateState on(DemoCreatedEvent event) {
	return new DemoAggregateState(event.getValue());
}

@EventSourcingHandler
DemoAggregateState on(DemoUpdatedEvent event, DemoAggregateState state) {
<strong>	state.setValue(event.getValue());
</strong>	return state;
}

@EventSourcingHandler
DemoAggregateState on(DemoDeletedEvent event, DemoAggregateState state) {
	state.setDeleted(true);
	return state;
}

</code></pre>
