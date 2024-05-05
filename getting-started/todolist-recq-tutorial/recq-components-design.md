---
description: Define your micorservices architecture structure.
---

# RECQ Components Design

Now that you have defined all the Messages you need to identify the components handling those messages.

We need to choose between:

* Aggregate
* Projector
* Projection
* Invoker
* Service
* Saga
* Observer

## [Aggregate](../../recq-patterns/recq-component-pattern/aggregate.md)

Let's start from the Domain logic handling aspects of the application, we have previously individuated the TodoList domain composed of the TodoList, Todo and User entities.

The component and also the pattern used to manage Domain Change Request is Aggregate which collect a group of entities in a Tree Relational Structure with a root representing the Consistency Constraint Boundaries and branches or leaves representing functional depending entities. A <mark style="color:blue;background-color:blue;">**TodoListAggregate**</mark> is needed to handle <mark style="color:blue;">TodoListCreateCommands</mark>, <mark style="color:blue;">TodoListDeleteCommand</mark>, <mark style="color:blue;">TodoListAddTodoCommand</mark>, <mark style="color:blue;">TodoListRemoveTodoCommand</mark>, <mark style="color:blue;">TodoListCheckTodoCommand</mark> and produce the related <mark style="color:orange;">events</mark> to communicate to the entire system that the state is changed.

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption><p>TodoList Aggregate (Pattern View)</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption><p>TodoList Aggregate Handlers</p></figcaption></figure>

## [Projector](../../recq-patterns/recq-component-pattern/projector.md)

Data changes must be materialized in some way, to create a database representing a practical and queryable system state we need to use a projector that handles Domain Events and writes changes inside a Repository. A <mark style="color:green;background-color:green;">**TodoListProjector**</mark> is needed to handle <mark style="color:orange;">TodoListCreatedEvents</mark>, <mark style="color:orange;">TodoListDeleteEvents</mark>, <mark style="color:orange;">TodoListTodoAddedEvent</mark>, <mark style="color:orange;">TodoListTosoRemovedEvent</mark>, <mark style="color:orange;">TodoListTodoCheckedEvent</mark> and materialize the changes.

<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption><p>TodoList Projector Handlers (igonre the ErpUserActivityRegisteredEvent will be added in the next tutorial)</p></figcaption></figure>

## [Projection](../../recq-patterns/recq-component-pattern/projection.md)

Then we need to access the system state and make queries to receive views, so we require a <mark style="color:green;background-color:green;">**TodoListProjection**</mark> to handle <mark style="color:yellow;">TodoListListItemViewFindAllQueries</mark> returning a collection of <mark style="color:green;">TodoListListItemView</mark> and <mark style="color:yellow;">TodoListViewFindByIdentifierQueries</mark> returning a <mark style="color:green;">TodoListView</mark>.

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>TodoList Projection Handlers</p></figcaption></figure>

## [Invoker](../../recq-patterns/recq-component-pattern/invoker.md)

In the end, we need a way to forge Commands and Queries accessible from the outside of a RECQ Architecture. To do this we need an invoker that exposes all the functions and implements logic (the Service Layer of the Layered Architecture). So we are gonna to define a **TodoListInvoker** generating payloads for every single TodoList-related command and query.

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption><p>TodoList Invoker handlers</p></figcaption></figure>

## [Service](../../recq-patterns/recq-component-pattern/service.md), [Saga ](../../recq-patterns/recq-component-pattern/saga.md)and [Observer](../../recq-patterns/recq-component-pattern/observer.md)

In this tutorial we do not need to handle cross-domain logic or do particular behaviour extensions, we will dedicate a specific tutorial to handle complex scenarios in RECQ Architectures. [extend-todolist-handle-complexity-tutorial](../extend-todolist-handle-complexity-tutorial/ "mention")

## Final Architecture

<figure><img src="../../.gitbook/assets/image (49).png" alt=""><figcaption><p>TodoList RECQ Architecture</p></figcaption></figure>

