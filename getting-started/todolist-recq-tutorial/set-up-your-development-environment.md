# Set up your Development Environment

Create a Spring Boot Application using Spring Initializr and assign Spring Web, Lombok, Spring data JPA, H2 Database.

```gradle
  implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
  implementation 'org.springframework.boot:spring-boot-starter-web'
  compileOnly 'org.projectlombok:lombok'
  runtimeOnly 'com.h2database:h2'
  annotationProcessor 'org.projectlombok:lombok'
  testImplementation 'org.springframework.boot:spring-boot-starter-test'
  annotationProcessor 'org.springframework.boot:spring-boot-configuration-processor'
```

Then add your Evento Framework Bundle Dependency and follow the [Quick Start](../quick-start.md) section to set up an Evento Server Instance.

```gradle
implementation group: 'com.eventoframework', name: 'evento-bundle', version: 'ev1.10.0'
```

### Evento Config

Instantiate the Evento Bundle Object as a Bean

```java
import com.eventoframework.demo.todo.TodoApplication;
import com.evento.application.EventoBundle;
import com.evento.application.bus.ClusterNodeAddress;
import com.evento.application.bus.EventoServerMessageBusConfiguration;
import com.evento.application.performance.TracingAgent;
import com.evento.common.modeling.messaging.message.application.Message;
import com.evento.common.modeling.messaging.message.application.Metadata;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class EventoConfig {

    @Bean
    public EventoBundle eventoBundle(BeanFactory factory) throws Exception {
        String bundleId = "ToDoList-Bundle";
        int bundleVersion = 1;
        var evento =  EventoBundle.Builder.builder()
                // Starting Package to detect RECQ components
                .setBasePackage(TodoApplication.class.getPackage())
                // Name of the bundle
                .setBundleId(bundleId)
                // Bundle's version
                .setBundleVersion(bundleVersion)
                // Set up the Evento message bus
                .setEventoServerMessageBusConfiguration(new EventoServerMessageBusConfiguration(
                        // Evento Server Addresses
                        new ClusterNodeAddress("localhost",3030)
                ))
                .setTracingAgent(new TracingAgent(bundleId, bundleVersion){
                    @Override
                    public Metadata correlate(Metadata metadata, Message<?> handledMessage) {
                        if(handledMessage!=null && handledMessage.getMetadata() != null && handledMessage.getMetadata().get("user") != null){
                            if(metadata == null) return handledMessage.getMetadata();
                            metadata.put("user", handledMessage.getMetadata().get("user"));
                            return metadata;
                        }
                        return super.correlate(metadata, handledMessage);
                    }})
                .setInjector(factory::getBean)
                .start();
        evento.getPerformanceService().setPerformanceRate(1);
        return evento;
    }
}
```
