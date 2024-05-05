# Test Your App

```
POST http://localhost:8080/todo-list/
Authorization: user1
Content-Type: application/json

{
  "name": "Sample Todo List"
}

> {%
    client.test("Request executed successfully (Created - 201)", function() {
        client.assert(response.status === 201, "Response status is not 201");
    });
 client.global.set("lastId", response.body.identifier)
 %}

###

POST http://localhost:8080/todo-list/{{lastId}}/todo/
Authorization: user1
Content-Type: application/json

{
  "content": "Simple Todo"
}

> {%
    client.test("Request executed successfully (No Content - 201)", function() {
        client.assert(response.status === 201, "Response status is not 201");
    });
    client.global.set("lastTodoId", response.body.identifier)
%}

###

GET http://localhost:8080/todo-list/{{lastId}}
Authorization: user1


> {%
    client.test("Request executed successfully (Ok - 200)", function() {
        client.assert(response.status === 200, "Response status is not 200");
    });
    client.test("Response correct", function() {

        client.assert(response.body.todos[0].identifier === client.global.get("lastTodoId"), "Wrong todo identifier");
    });
    console.log(response)
%}


###

DELETE http://localhost:8080/todo-list/{{lastId}}/todo/{{lastTodoId}}
Authorization: user1


> {%
    client.test("Request executed successfully (Ok - 204)", function() {
        client.assert(response.status === 204, "Response status is not 204");
    });
%}

###

GET http://localhost:8080/todo-list/{{lastId}}
Authorization: user1


> {%
    client.test("Request executed successfully (Ok - 200)", function() {
        client.assert(response.status === 200, "Response status is not 200");
    });
    client.test("Response correct", function() {

        client.assert(response.body.todos.length === 0, "TodoList not updates");
    });
    console.log(response)
%}

###

POST http://localhost:8080/todo-list/{{lastId}}/todo/
Authorization: user1
Content-Type: application/json

{
  "content": "Simple Todo"
}

> {%
    client.test("Request executed successfully (No Content - 201)", function() {
        client.assert(response.status === 201, "Response status is not 201");
    });
    client.global.set("lastTodoId", response.body.identifier)
%}

###

PUT http://localhost:8080/todo-list/{{lastId}}/todo/{{lastTodoId}}
Authorization: user1

> {%
    client.test("Request executed successfully (No Content - 202)", function() {
        client.assert(response.status === 202, "Response status is not 202");
    });
%}


###

DELETE http://localhost:8080/todo-list/{{lastId}}/todo/{{lastTodoId}}
Authorization: user1

> {%
    client.test("Request executed successfully (No Content - 500)", function() {
        client.assert(response.status === 500, "Response status is not 500");
    });
%}

###

DELETE http://localhost:8080/todo-list/{{lastId}}
Authorization: user1

> {%
    client.test("Request executed successfully (No Content - 500)", function() {
        client.assert(response.status === 500, "Response status is not 500");
    });
%}
```
