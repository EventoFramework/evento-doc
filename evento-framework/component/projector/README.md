# @Projector

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
public @interface Projector {
    int version();
}
```

```java
package org.evento.demo.query;

import org.evento.common.modeling.annotations.component.Projector;

@Projector(version = 2)
public class DemoMongoProjector {

	private final DemoMongoRepository demoMongoRepository;

	public DemoMongoProjector(DemoMongoRepository demoMongoRepository) {
		this.demoMongoRepository = demoMongoRepository;
	}
	
	/** Event Handlers **/
}
```
