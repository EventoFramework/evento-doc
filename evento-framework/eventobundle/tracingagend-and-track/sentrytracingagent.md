---
description: A Deep Dive into Custom Tracing with Sentry
---

# SentryTracingAgent

The code provided showcases `SentryTracingAgent`, a custom implementation of the `TracingAgent` class in Evento. This agent leverages the Sentry platform for distributed tracing, offering a more comprehensive tracing solution compared to the default implementation. Let's delve into how `SentryTracingAgent` works and overrides core methods.

```java
import io.sentry.*;
import io.sentry.exception.InvalidSentryTraceHeaderException;
import com.evento.application.performance.TracingAgent;
import com.evento.application.performance.Track;
import com.evento.common.modeling.messaging.message.application.*;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.stream.Stream;

import static io.sentry.BaggageHeader.BAGGAGE_HEADER;
import static io.sentry.SentryTraceHeader.SENTRY_TRACE_HEADER;

public class SentryTracingAgent extends TracingAgent {

    public SentryTracingAgent(String bundleId, long bundleVersion, String sentryDns) {
        super(bundleId, bundleVersion);
        Sentry.init(options -> {
            options.setDsn(sentryDns);
            options.setEnableTracing(true);
            options.setTracesSampleRate(1.0);
        });
    }

    @SuppressWarnings("unchecked")
    @Override
    protected <T> T doTrack(Message<?> message, String component,
                            Track trackingAnnotation,
                            Transaction<T> transaction) throws Exception {
        if (message == null) return transaction.run();
        var metadata = message.getMetadata();
        if (metadata == null) {
            metadata = new Metadata();
        }
        ITransaction t;
        var action = switch (message) {
            case CommandMessage<?> ignored -> "handleCommand";
            case QueryMessage<?>  ignored -> "handleQuery";
            case EventMessage<?>  ignored -> "onEvent";
            case InvocationMessage i -> i.getAction();
            default -> "invoke";
        };
        if (metadata.containsKey(SENTRY_TRACE_HEADER)) {
            try {
                t = Sentry.startTransaction(
                        TransactionContext.fromSentryTrace(
                                component + "." + action + "(" + message.getPayloadName() + ")",
                                "evento",
                                new SentryTraceHeader(
                                        metadata.get(SENTRY_TRACE_HEADER)
                                )
                        )
                );
            } catch (InvalidSentryTraceHeaderException e) {
                return transaction.run();

            }
        } else {
            if (trackingAnnotation != null) {

                t = Sentry.startTransaction(
                        component + "." + action + "(" + message.getPayloadName() + ")",
                        "evento");
            } else {
                try {
                    return transaction.run();
                } catch (Exception e) {
                    if (e.getCause() instanceof RuntimeException re) {
                        re.setStackTrace(Stream.concat(
                                Stream.of(re.getStackTrace()),
                                Stream.of(new RuntimeException().getStackTrace())
                        ).toArray(StackTraceElement[]::new));
                        throw re;
                    }
                    throw e;
                }

            }
        }
        metadata.put(SENTRY_TRACE_HEADER, t.toSentryTrace().getValue());
        var b = t.toBaggageHeader(List.of());
        if (b != null)
            metadata.put(BAGGAGE_HEADER, b.getValue());
        t.setData("Description", t.getName() + " - " + getBundleId() + "@" + getBundleVersion());
        t.setTag("message", message.getPayloadName());
        t.setTag("component", component);
        t.setTag("bundle", getBundleId());
        t.setTag("bundleVersion", String.valueOf(getBundleVersion()));
        if (message instanceof DomainCommandMessage cm) {
            t.setData("AggregateId", cm.getAggregateId());
        }
        message.setMetadata(metadata);
        try {
            var resp = transaction.run();
            if (resp instanceof CompletableFuture<?> c) {
                resp = (T) c.thenApply(o -> {
                    t.finish(SpanStatus.OK);
                    return o;
                }).exceptionally(tr -> {
                    t.setThrowable(tr);
                    t.setData("Payload", message.getSerializedPayload().getSerializedObject());
                    t.finish(SpanStatus.INTERNAL_ERROR);
                    Sentry.captureException(tr);
                    System.out.println(t.toSentryTrace().getTraceId());
                    throw new CompletionException(tr);
                });
            } else {
                t.finish(SpanStatus.OK);
            }
            return resp;
        } catch (Throwable tr) {
            t.setThrowable(tr);
            t.setData("Pyload", message.getSerializedPayload().getSerializedObject());
            t.finish(SpanStatus.INTERNAL_ERROR);
            Sentry.captureException(tr);
            System.out.println(t.toSentryTrace().getTraceId());
            throw tr;
        }
    }

    @Override
    public Metadata correlate(Metadata metadata, Message<?> handledMessage) {
        if (handledMessage == null)
            return metadata;
        if (handledMessage.getMetadata() != null && handledMessage.getMetadata().containsKey(SENTRY_TRACE_HEADER)) {
            if (metadata == null) {
                metadata = new Metadata();
            }
            metadata.put(SENTRY_TRACE_HEADER, handledMessage.getMetadata().get(SENTRY_TRACE_HEADER));
        }
        if (handledMessage.getMetadata() != null && handledMessage.getMetadata().containsKey(BAGGAGE_HEADER)) {
            if (metadata == null) {
                metadata = new Metadata();
            }
            metadata.put(BAGGAGE_HEADER, handledMessage.getMetadata().get(BAGGAGE_HEADER));
        }
        return metadata;
    }


}
```

**Initialization with Sentry DSN:**

The constructor accepts the bundle ID, version, and a crucial parameter - `sentryDns`. This DSN (Data Source Name) is used to configure the Sentry SDK for communication with your Sentry instance.

**Overridden `doTrack` Method:**

This method is the heart of the tracing functionality. Here's a breakdown of its behavior:

1. **Message and Metadata Check:** It first checks if a message is provided. If not, the transaction is executed without tracing. It then retrieves the message's metadata for further processing.
2. **Transaction Initiation:**
   * The code utilizes a switch statement to identify the message type (command, query, event, or invocation) based on the message class.
   * Depending on the message type and the presence of a `SENTRY_TRACE_HEADER` in the metadata, it initiates a new transaction using the Sentry SDK.
     * If the header exists, it attempts to create a transaction from the provided trace information.
     * In its absence, it creates a new transaction with a descriptive name based on the message type, component, and payload name. The `@Track` annotation presence also influences transaction creation.
3. **Metadata Enrichment:**
   * The `SENTRY_TRACE_HEADER` and, optionally, the `BAGGAGE_HEADER` are added to the message's metadata for propagation across services.
   * Additional data is attached to the transaction using Sentry's `setData` and `setTag` methods. This data includes information about the bundle, message, and component involved.
   * For `DomainCommandMessage` objects, the `AggregateId` is also captured.
4. **Transaction Completion and Error Handling:**
   * The actual transaction logic is wrapped within a `try-catch` block.
   * For successful completions, the transaction is marked as finished with `SpanStatus.OK`.
   * If an exception occurs:
     * The exception is set on the transaction using `setThrowable`.
     * The message payload is captured as transaction data using `setData("Payload", message.getSerializedPayload().getSerializedObject())`.
     * The transaction is marked as finished with `SpanStatus.INTERNAL_ERROR`.
     * The exception is captured by Sentry using `Sentry.captureException`.
     * The trace ID is printed for debugging purposes.
     * The exception is then re-thrown.
   * The `CompletableFuture` scenario is handled specifically. The returned `CompletableFuture` is transformed to capture the successful result or any exceptions that might occur asynchronously. In case of exceptions, the transaction is finalized with appropriate status and the exception is re-thrown as a `CompletionException`.

**Overridden `correlate` Method:**

This method extracts the `SENTRY_TRACE_HEADER` and `BAGGAGE_HEADER` (if present) from the provided `handledMessage` and merges them into the existing `metadata`. This ensures proper context propagation between messages.

**Key Advantages of SentryTracingAgent:**

* **Integration with Sentry:** Leverages the feature-rich Sentry platform for distributed tracing, providing valuable insights into application behavior across services.
* **Enhanced Correlation:** Extracts trace and baggage headers from messages for improved context propagation.
* **Detailed Spans:** Captures message type, component, bundle information, and payload data within Sentry spans.
* **Error Handling and Reporting:** Captures exceptions and message payloads for better error analysis within Sentry.

**In essence, SentryTracingAgent empowers developers with a powerful tool for distributed tracing within Evento applications. By leveraging Sentry's capabilities, you gain a deeper understanding of how your application functions, identify performance bottlenecks, and effectively troubleshoot issues.**
