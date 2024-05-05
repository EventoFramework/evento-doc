---
description: >-
  Now that we have the domain and all the functional requirements we can design
  our Payloads.
---

# RECQ Payload Design

To design a RECQ architecture we need to define the four main payloads that describe actions and data.&#x20;

To do this we need to follow the [RECQ Communication Pattern](../../recq-patterns/recq-communication-pattern/) that forces us to describe our system's interactions in terms of distinguished message classes: Commands, Events, Queries and Views.

By analysing each requirement and given the domain we can define these payloads:

* As a user, I want to create a to-do list to fill it with todos.
  * <mark style="background-color:blue;">TodoListCreateCommand</mark>
  * <mark style="background-color:orange;">TodoListCreatedEvent</mark>
* As a user, I want to delete a to-do list that does not contain checked todos because now is useless.
  * <mark style="background-color:blue;">TodoListDeleteCommand</mark>
  * <mark style="background-color:orange;">TodoListDeleteEvent</mark>
* As a user, I want to add a to-do inside a to-do list to check it later.
  * <mark style="background-color:blue;">TodoListAddTodoCommand</mark>
  * <mark style="background-color:orange;">TodoListTodoAddedEvent</mark>
* As a user, I want to remove a todo from a todo list because it will never be checked.
  * <mark style="background-color:blue;">TodoListRemoveTodoCommand</mark>
  * <mark style="background-color:orange;">TodoListTosoRemovedEvent</mark>
* As a user, I want to check a to-do inside a to-do list to mark it as done.
  * <mark style="background-color:blue;">TodoListCheckTodoCommand</mark>
  * <mark style="background-color:orange;">TodoListTodoCheckedEvent</mark>
* As a user, I want to get a list of all the Todo Lists in the systems to explore them.
  * <mark style="background-color:yellow;">TodoListListItemViewFindAllQuery</mark>
  * <mark style="background-color:green;">TodoListListItemView</mark>
* As a user, I want to get the details of a to-do list to know every to-do status.
  * <mark style="background-color:yellow;">TodoListViewFindByIdentifierQuery</mark>
  * <mark style="background-color:green;">TodoListView</mark>

