# Projector @EventHandler

```java
package org.evento.demo.query;
import org.evento.common.modeling.annotations.handler.EventHandler;
//...

@EventHandler
void on(DemoCreatedEvent event, 
		QueryGateway queryGateway, 
		EventMessage eventMessage) {
	var now = Instant.now();
	demoMongoRepository.save(new DemoMongo(event.getDemoId(),
			event.getName(),
			event.getValue(), now, now, null));
}

@EventHandler
void on(DemoUpdatedEvent event) {
	demoMongoRepository.findById(event.getDemoId()).ifPresent(d -> {
		d.setName(event.getName());
		d.setValue(event.getValue());
		d.setUpdatedAt(Instant.now());
		demoMongoRepository.save(d);
	});
}
```
