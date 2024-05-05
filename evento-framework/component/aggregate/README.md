# @Aggregate

WIP

```java
package org.evento.common.modeling.annotations.component;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE})
@Component
public @interface Aggregate {
    int snapshotFrequency() default -1;
}

```

```java
import org.evento.common.modeling.annotations.component.Aggregate;

@Aggregate(snapshotFrequency = 10)
public class DemoAggregate {
    /** Command Handlers, Event Sourcing Handlers **/
}
```
