# View

WIP

```java
package org.evento.common.modeling.messaging.payload;

public abstract class View extends Payload {
}

```

```java
package org.evento.demo.api.view;
import org.evento.common.modeling.messaging.payload.View;

public class DemoView extends View {
	private String demoId;
	private String name;
	private Long value;
	
	/** Getter, Setter, Constructors **/	
}
```

```java
package org.evento.demo.api.view;

import org.evento.common.modeling.messaging.payload.View;

public class DemoRichView extends View {

	private String demoId;
	private String name;
	private Long value;
	private long createdAt;
	private long updatedAt;
	private Long deletedAt;
	
	/** Getter, Setter, Constructors **/	
}
```
