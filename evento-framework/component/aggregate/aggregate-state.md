# Aggregate State

```java
package org.evento.common.modeling.state;

import java.io.Serializable;

public abstract class AggregateState implements Serializable {
    private boolean deleted = false;

    /** Getter, Setter, Constructors **/	
}
```

```java
package org.evento.demo.command.aggregate;

import org.evento.common.modeling.state.AggregateState;

public class DemoAggregateState extends AggregateState {
	private long value;
	
	/** Getter, Setter, Constructors **/	
}
```
