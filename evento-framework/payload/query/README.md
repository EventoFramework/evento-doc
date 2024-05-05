# Query

WIP

<pre class="language-java"><code class="lang-java">package org.evento.common.modeling.messaging.payload;

<strong>import org.evento.common.modeling.messaging.query.QueryResponse;
</strong>import java.lang.reflect.ParameterizedType;

public abstract class Query&#x3C;T extends QueryResponse&#x3C;?>> extends Payload {

	public Class&#x3C;T> getResponseType() {
		return (Class&#x3C;T>) ((ParameterizedType) ((ParameterizedType) getClass()
				.getGenericSuperclass()).getActualTypeArguments()[0])
				.getRawType();
	}
}
</code></pre>

```java
package org.evento.demo.api.query;

import org.evento.common.modeling.messaging.payload.Query;
import org.evento.common.modeling.messaging.query.Multiple;
import org.evento.demo.api.view.DemoRichView;

public class DemoRichViewFindAllQuery extends Query<Multiple<DemoRichView>> {

	private String filter;
	private String sort;
	private Integer limit;
	private Integer offset;
	
	/** Getter, Setter, Constructors **/	
}
```
