---
description: The Todo List
---

# Problem Description and Requirement Gathering

We need to implement a Todo list application, only the backend in terms of REST API.

### Problem Description

We need to implement a Todo List app where a user can create Todo Lists. Each Todo list has a name. Each Todo list contains a collection of a maximum of five todos with a proper description and a checked flag. Once a todo is checked we cannot delete or edit it and also we cannot delete the Todo list containing it. We want to keep auditing each action knowing who has created or edited a to-do list and each contained todo.

<figure><img src="../../.gitbook/assets/Diagramma senza titolo (1).jpg" alt=""><figcaption><p>Todo list concept</p></figcaption></figure>

### Requirement Gathering

To analyse the problem we need to decompose the description in a list of requirements. Let's split the analysis into two sides: Domain and Constrains, in the next chapter we will see another technique.

#### Domain

Starting from the prompt we need to individuate all the entities involving the domain:

> We need to implement a <mark style="background-color:purple;">Todo List</mark> app where a user can create <mark style="background-color:purple;">Todo Lists</mark>. Each <mark style="background-color:purple;">Todo list</mark> has a <mark style="color:purple;">name</mark>. Each <mark style="background-color:purple;">Todo list</mark> <mark style="color:purple;">contains a collection</mark> of a maximum of five <mark style="background-color:blue;">todos</mark> with a proper <mark style="color:blue;">description</mark> and a <mark style="color:blue;">checked flag</mark>. Once a <mark style="background-color:blue;">todo</mark> is checked we cannot delete or edit it and also we cannot delete the <mark style="background-color:purple;">Todo list</mark> containing it. We want to keep <mark style="color:orange;">auditing each action</mark> knowing <mark style="background-color:green;">who</mark> has <mark style="color:orange;">created or edited</mark> a <mark style="background-color:purple;">to-do list</mark> and each contained <mark style="background-color:blue;">todo</mark>.

By a term inspection, we can individuate three entities: <mark style="background-color:purple;">TodoList</mark>, <mark style="background-color:blue;">Todo</mark> and <mark style="background-color:green;">User.</mark>

***

With a second inspection, we can define properties and relations between entities:

* TodoList
  * <mark style="color:purple;">name</mark> - the list name
  * <mark style="color:purple;">todos</mark> - the collection of Todo
* Todo
  * <mark style="color:blue;">description</mark> -the todo description
  * <mark style="color:blue;">checked</mark> - the flag indicating the completion
* User
  * <mark style="color:green;">identifier</mark> - we do not have enough information about it we can use the username

***

In the end, we need to identify non-functional fields and technical ones.

* TodoList
  * <mark style="color:purple;">identifier -</mark> the list UUID
  * <mark style="color:purple;">name</mark> - the list name
  * <mark style="color:purple;">todos</mark> - the collection of Todo
  * <mark style="color:orange;">createdAt</mark> - creation audit
  * <mark style="color:orange;">createdBy</mark> - creation audit
  * <mark style="color:orange;">updatedAt</mark> - update audit
  * <mark style="color:orange;">updatedBy</mark> - update audit
* Todo
  * <mark style="color:blue;">identifier</mark> <mark style="color:purple;">-</mark> the todo UUID
  * <mark style="color:blue;">description</mark> -the todo description
  * <mark style="color:blue;">checked</mark> - the flag indicating the completion
  * <mark style="color:orange;">createdAt</mark> - creation audit
  * <mark style="color:orange;">createdBy</mark> - creation audit
  * <mark style="color:orange;">checkedAt</mark> - check audit
  * <mark style="color:orange;">checkedBy</mark> - check audit
* User
  * <mark style="color:green;">identifier</mark> - we do not have enough information about it we can use the username

***

#### Functional Requirements

Once we've analysed our domain and all the information let's express and formalize any requirement in the form of user stories:

* As a user, I want to create a to-do list in order to fill it with todos.
* As a user, I want to delete a to-do list that does not contain checked todos because now is useless.
* As a user, I want to add a to-do inside a to-do list to check it later.
* As a user, I want to remove a todo from a todo list because it will never be checked.
* As a user, I want to check a to-do inside a to-do list to mark it as done.
* As a user, I want to get a list of all the Todo Lists in the systems to explore them.
* As a user, I want to get the details of a to-do list in order to know every todo status.

