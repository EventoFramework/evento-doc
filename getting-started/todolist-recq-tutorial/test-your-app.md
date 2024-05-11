---
description: Testing the TodoList App with Evento and Spring Frameworks
---

# Test Your App

This chapter dives into how to test the TodoList application built using the Evento Framework and Spring Framework. We'll explore writing automated tests to ensure the functionality of your application.

#### Tools and Technologies

* **Testing Framework:** We'll assume you're using a popular testing framework like RestAssured or Spring Boot Test.
* **Evento Framework:** This framework provides functionalities for building APIs.
* **Spring Framework:** This framework provides dependency injection and other features for building robust applications.

#### Testing Approach

Our testing strategy focuses on API endpoints related to TodoList management. We'll follow a pattern of:

1. **Sending a request:** Simulate an HTTP request (like POST, GET, PUT, or DELETE) with specific headers and body content.
2. **Verifying the response:** Assert the expected HTTP status code and potentially validate the response body.
3. **Storing information:** Capture relevant information from the response body for use in subsequent tests.

#### Sample Tests

Here are some examples showcasing how to test different functionalities of the TodoList application:

**1. Creating a TodoList:**

```java
// Assuming RestAssured is used for testing

// Prepare the request body
String todoListName = "Sample Todo List";
String requestBody = "{\"name\":\"" + todoListName + "\"}";

// Send the request and capture the response
Response response = RestAssured.given()
    .auth().oauth2("user1")
    .header("Content-Type", "application/json")
    .body(requestBody)
.post("http://localhost:8080/todo-list/");

// Verify response status and store ID
response.then().assertThat().statusCode(201);
String todoListId = response.getBody().jsonPath().getString("identifier");

// Store the ID for later use
client.global.set("lastId", todoListId);
```

**2. Creating a Todo Item:**

```java
// Assuming you have a stored lastId from previous test

String todoContent = "Simple Todo";
String requestBody = "{\"content\":\"" + todoContent + "\"}";

response = RestAssured.given()
    .auth().oauth2("user1")
    .header("Content-Type", "application/json")
    .body(requestBody)
.post("http://localhost:8080/todo-list/" + client.global.get("lastId") + "/todo/");

response.then().assertThat().statusCode(201);
String todoItemId = response.getBody().jsonPath().getString("identifier");
client.global.set("lastTodoId", todoItemId);
```

**3. Getting a TodoLists**

```java
// Assuming you have a stored lastId

response = RestAssured.given()
    .auth().oauth2("user1")
.get("http://localhost:8080/todo-list/" + client.global.get("lastId"));

response.then().assertThat().statusCode(200);
// Assert the retrieved todo list contains the created todo item
// ... (using response.body)
```

**4. Deleting a Todo Item:**

```java
// Assuming you have stored lastId and lastTodoId

response = RestAssured.given()
    .auth().oauth2("user1")
.delete("http://localhost:8080/todo-list/" + client.global.get("lastId") + "/todo/" + client.global.get("lastTodoId"));

response.then().assertThat().statusCode(204); // No Content expected
```

**5. Additional Considerations:**

* You can write tests for PUT requests to update existing to-do items.
* Implement negative test scenarios (e.g., unauthorized access, invalid data).
* Consider using data providers to create different test cases with varied input data.

**Remember:**

* Replace `"user1"` with the appropriate authentication token for your application.
* Adapt the assertions (`... (using response.body)`) in step 3 to validate the specific response structure of your TodoList object.
