# Single

WIP

```java
package org.evento.common.modeling.messaging.query;

import org.evento.common.modeling.messaging.payload.View;

public class Single<T extends View> extends QueryResponse<T> {

	private T data;

	public static <R extends View> Single<R> of(R data) {
		var r = new Single<R>();
		r.setData(data);
		return r;
	}
	
	/** Getter, Setter, Constructors **/	
}
```
