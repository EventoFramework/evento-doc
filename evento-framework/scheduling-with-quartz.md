---
description: Deadlines and scheduled commands belong to the domain; Quartz runs them, Evento delivers them exactly once
---

# Scheduling and Deadlines with Quartz

Evento has no deadline manager and no scheduled events, by design. "Cancel the order if it is not paid in 30 minutes", "send the reminder on Monday" are business rules: when they fire, what they do, whether they are cancelled. They belong in the domain, where they can be read, tested and changed with the rest of it, and a scheduler is a solved problem. Use [Quartz](https://www.quartz-scheduler.org/) in a bundle and let the job send a command.

What Evento gives the job: a `CommandGateway`, and an **idempotency key**, so a job that fires twice (a retry after a crash, two scheduler nodes) still changes the aggregate once.

## The pattern

1. Something in the domain decides there is a deadline: usually a saga or a service handling the event that starts the clock (`OrderPlaced`).
2. It schedules a Quartz job with the data the command needs (the order id), its trigger time, and a job key derived from the business identity (`payment-deadline:<orderId>`), so scheduling twice does not create two jobs.
3. When it fires, the job sends the command with `sendIdempotent`, the key derived from the same identity.
4. The aggregate decides: an order already paid ignores (or refuses) `ExpireOrder`. The deadline never needs to be "cancelled" for correctness; cancelling it (deleting the job when `OrderPaid` arrives) only saves work.

```java
public class OrderDeadlineJob implements Job {

    // Quartz builds jobs itself: take the gateway from the scheduler context.
    @Override
    public void execute(JobExecutionContext ctx) throws JobExecutionException {
        String orderId = ctx.getMergedJobDataMap().getString("orderId");
        try {
            CommandGateway commands = (CommandGateway) ctx.getScheduler().getContext().get("commands");
            commands.sendIdempotent(new ExpireOrder(orderId), "payment-deadline:" + orderId)
                    .get(30, TimeUnit.SECONDS);
        } catch (Exception e) {
            // Quartz runs it again; the key makes the retry a replay, not a second expiry.
            throw new JobExecutionException(e, true);
        }
    }
}
```

```java
@Saga(version = 1)
public class PaymentDeadlineSaga {

    private final Scheduler scheduler;

    // The Quartz scheduler comes from the bundle's injector (or a Spring bean with the starter).
    public PaymentDeadlineSaga(Scheduler scheduler) {
        this.scheduler = scheduler;
    }

    @SagaEventHandler(init = true, associationProperty = "orderId")
    PaymentDeadlineState on(OrderPlaced event) throws SchedulerException {
        var job = JobBuilder.newJob(OrderDeadlineJob.class)
                .withIdentity("payment-deadline:" + event.getOrderId())
                .usingJobData("orderId", event.getOrderId())
                .build();
        var trigger = TriggerBuilder.newTrigger()
                .startAt(Date.from(event.getPlacedAt().plus(Duration.ofMinutes(30))))
                .build();
        if (!scheduler.checkExists(job.getKey())) scheduler.scheduleJob(job, trigger);
        return new PaymentDeadlineState();
    }

    @SagaEventHandler(associationProperty = "orderId")
    PaymentDeadlineState on(OrderPaid event, PaymentDeadlineState state) throws SchedulerException {
        scheduler.deleteJob(JobKey.jobKey("payment-deadline:" + event.getOrderId()));
        state.setEnded(true);
        return state;
    }
}
```

The `Scheduler` reaches the saga like any other dependency of a component, through its constructor (the [injector](eventobundle/injector-and-component.md), or a Spring bean with the [starter](eventobundle/spring-boot-starter.md)); put it in the scheduler context too (`scheduler.getContext().put("commands", commandGateway)`) for the job.

## Making it reliable

* **Persist the jobs**: Quartz's JDBC job store (`org.quartz.jobStore.class = org.quartz.impl.jdbcjobstore.JobStoreTX`), on the bundle's own database, so deadlines survive restarts.
* **Run several instances**: `org.quartz.jobStore.isClustered = true`. Quartz then fires each trigger on one instance, and takes over the triggers of an instance that died. The idempotency key covers the rare double fire.
* **Misfires**: decide what a deadline missed while every instance was down means for the business (`withMisfireHandlingInstructionFireNow()` fires it as soon as possible).
* **Consumer replays**: a saga replayed from an earlier checkpoint schedules again; the job key derived from the business identity, and `checkExists`, keep it to one job.
* **Clock**: triggers use the scheduler's clock. Compute the time from the event's own timestamp, as above, not from the moment the handler runs, so a consumer catching up does not push deadlines later.

## Why not in the framework

A framework deadline manager would need its own store, its own clustering and its own operations, all of which Quartz (and others: db-scheduler, JobRunr, the cloud schedulers) already have and operators already know. Evento's job is to deliver the command once and to keep the domain in charge of what it means; scheduled events and framework deadlines would hide business rules inside infrastructure.
