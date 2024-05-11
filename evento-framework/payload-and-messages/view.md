# Query and View

The Evento Framework empowers you to build robust and scalable applications with its well-defined approach to handling queries. This section delves into the core concepts of Query Payloads and Messages, providing the foundation for effective data retrieval within your Evento applications.

By leveraging these concepts, you can design a clear separation between your queries and their corresponding response structures. This improves code readability, and maintainability, and promotes a consistent communication pattern within your microservices architecture.

#### Source Code Breakdown

The following code snippets showcase the key Evento classes involved in query handling:

**1. Query Interface (Query.java):**

```java
import com.evento.common.modeling.messaging.query.QueryResponse;

import java.lang.reflect.ParameterizedType;


/**
 * The Query interface represents a query object that can be sent to a system to retrieve a response.
 * It extends the Payload interface.
 *
 * @param <T> The type of QueryResponse expected as the response.
 */
public interface Query<T extends QueryResponse<?>> extends Payload {

	/**
	 * Returns the response type of the Query.
	 *
	 * @return The Class object representing the response type.
	 */
	@SuppressWarnings("unchecked")
	public default Class<T> getResponseType() {
		return (Class<T>) ((ParameterizedType) ((ParameterizedType) getClass()
				.getGenericSuperclass()).getActualTypeArguments()[0]).getRawType();
	}
}
```

The `Query` interface establishes the foundation for building queries. It enforces the `Payload` interface, indicating that queries carry data. The generic type parameter `T` allows you to specify the expected response type (`QueryResponse`). The `getResponseType()` method leverages generics to determine the Class object representing the expected response data structure.

**2. QueryMessage (QueryMessage.java):**

```java
import com.evento.common.modeling.messaging.payload.Query;

/**
 * The QueryMessage class represents a message containing a query.
 *
 * @param <T> The type of the query payload.
 */
public class QueryMessage<T extends Query<?>> extends Message<T> {
	/**
	 * The QueryMessage class represents a message containing a query.
	 *
     * @param payload The Query payload
     */
	public QueryMessage(T payload) {
		super(payload);
	}

	/**
	 * The QueryMessage class represents a message containing a query.
	 * It is a subclass of the Message class and is generically typed with a Query payload.
	 * The QueryMessage class provides methods to retrieve the query name and query payload.
	 *
     */
	public QueryMessage() {
	}


	/**
	 * Retrieves the name of the query.
	 *
	 * @return The name of the query as a String.
	 */
	public String getQueryName() {
		return super.getPayloadName();
	}
}
```

The `QueryMessage` class acts as a container for `Query` objects. It inherits from the `Message` class, providing functionalities for message routing and handling. Additionally, it retrieves the query name from the underlying payload (if it has a name).

**3. QueryResponse (QueryResponse.java):**

```javascript
import com.evento.common.modeling.messaging.payload.View;

import java.io.Serializable;

/**
 * The QueryResponse class is an abstract class that represents a response object for a query.
 * It is Serializable, which means it can be converted into a byte stream and sent over a network or stored in a file.
 * The class is generic, with a type parameter T that must extend the View class.
 * It provides methods to set and retrieve the data from the response.
 *
 * @param <T> The type of view the QueryResponse object contains.
 */
public abstract class QueryResponse<T extends View> implements Serializable {


}
```

```java
import com.evento.common.modeling.messaging.payload.View;

/**
 * Creates a new instance of the Single class.
 * @param <T> the view response of a query
 */
public class Single<T extends View> extends QueryResponse<T> {

    private T data;

    /**
     * The Single class represents a response containing a single view object.
     * It extends the QueryResponse class.
     * <p>
     * This class is generic and the type parameter T must extend the View class.
     * It provides methods to set and retrieve the data from the response.
     */
    public Single() {
    }

    /**
     * Creates a new Single object with the given data.
     *
     * @param <R>  the type of the data in the response, must extend the View class
     * @param data the data to set in the response
     * @return the Single object with the provided data
     */
    public static <R extends View> Single<R> of(R data) {
       var r = new Single<R>();
       r.setData(data);
       return r;
    }

    /**
     * Retrieves the data stored in the response object.
     *
     * @return the data stored in the response object
     */
    public T getData() {
       return data;
    }

    /**
     * Sets the data in the response object.
     *
     * @param data the data to be set in the response object. It must extend the View class.
     */
    public void setData(T data) {
       this.data = data;
    }


}
```

```java
import com.evento.common.modeling.messaging.payload.View;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * Represents a response object that contains multiple instances of a specified type.
 * Extends the `QueryResponse` class.
 *
 * @param <T> The type of view the Multiple object contains.
 */
public class Multiple<T extends View> extends QueryResponse<T> {

    private Collection<T> data;

    /**
     * Represents a response object that contains multiple instances of a specified type.
     * Extends the `QueryResponse` class.
     *
     */
    public Multiple() {
    }

    /**
     * Constructs a new Multiple object containing multiple instances of a specified type.
     *
     * @param <R> The type of view the Multiple object contains.
     * @param data The collection of views to be contained in the Multiple object.
     * @return A new Multiple object containing the specified views.
     */
    public static <R extends View> Multiple<R> of(Collection<R> data) {
       var r = new Multiple<R>();
       r.setData(new ArrayList<>(data));
       return r;
    }

    /**
     * Constructs a new Multiple object containing multiple instances of a specified type.
     *
     * @param <R> The type of view the Multiple object contains.
     * @param items The array of views to be contained in the Multiple object.
     * @return A new Multiple object containing the specified views.
     */
    @SafeVarargs
    public static <R extends View> Multiple<R> of(R... items) {
       var r = new Multiple<R>();
       r.setData(List.of(items));
       return r;
    }

    /**
     * Retrieves the data contained in the Multiple object.
     *
     * @return The collection of views contained in the Multiple object.
     */
    public Collection<T> getData() {
       return data;
    }

    /**
     * Sets the data for the Multiple object.
     *
     * @param data The collection of views to be set as the data for the Multiple object.
     */
    public void setData(Collection<T> data) {
       this.data = data;
    }

}
```

The `QueryResponse` class serves as an abstract base class for all query response objects. It enforces data serialization by implementing `Serializable`. The generic type parameter `T` restricts the response data type to extend the `View` interface (discussed later). Concrete implementations like `Single<T>` and `Multiple<T>` cater to different response scenarios:

* `Single<T>`: Used for responses containing a single `View` object.
* `Multiple<T>`: Used for responses containing a collection of `View` objects (e.g., list of todos).

**4. View Interface (View.java):**

```java
/**
 * The View interface represents a view object that can be used in a software system.
 * It extends the Payload interface.
 */
public interface View extends Payload {
}
```

The `View` interface represents a simple data transfer object (DTO) used for transporting data within the Evento Framework. It extends the `Payload` interface, signifying it carries data. Views are essentially plain data structures that can be serialized for efficient network transmission.

**Putting it Together:**

By combining these components, you can design clear and well-defined queries along with their expected response structures. Here's an example demonstrating this concept:

Java

```java
// Define a Query to retrieve all Todo items
public class GetAllTodosQuery implements Query<Multiple<TodoView>> {
  // ... query logic
}

// Define a View for Todo data
public class TodoView implements View {
  private String id;
  private String name;
  // ... other Todo properties
  // Getters and Setters
}
```

In this example, the `GetAllTodosQuery` expects a response containing a collection of `TodoView` objects using the `Multiple` class. This structure clearly communicates the query's purpose and the format of the anticipated response.

By leveraging Evento's Query Payloads and Messages, you can create well-organized and maintainable applications that effectively handle data retrieval across your microservices architecture.
