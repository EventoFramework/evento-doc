# GUI Auth

#### The Initial Encounter: A Token Request

Upon launching the Evento GUI for the first time, you'll be greeted by a login screen, acting as the first line of defense. Unlike traditional username and password combinations, the Evento GUI employs a token-based authentication system. This mechanism ensures secure access by requiring a temporary token issued by the Evento server itself.

The login screen will prominently display an alert message, informing you that a token is required for access. This message serves as a clear reminder that unauthorized access attempts are futile.

<figure><img src="../.gitbook/assets/image (52).png" alt=""><figcaption></figcaption></figure>

#### Unveiling the Token: A Journey Through Application Logs

To gain access to the coveted token, you'll need to embark on a brief exploration of the Evento server's application logs. These logs serve as a detailed record of the server's activities, often containing valuable pieces of information.

Within the application logs, keep an eye out for entries related to token generation. These entries might be marked with specific keywords or phrases like "Web Token" or "API Token Generation." The exact format and location of these entries might vary depending on your specific Evento server configuration.

Once you locate a relevant log entry, it will typically contain the actual token string. This string is a unique identifier that grants temporary access to the Evento GUI. Remember to treat this token with care, as it serves as your key to unlocking the hidden world of your distributed system.

<figure><img src="../.gitbook/assets/image (51).png" alt=""><figcaption></figcaption></figure>

#### Granting Access: The Power of the Token

Armed with the token obtained from the application logs, return to the Evento GUI login screen. Locate the designated field for entering the token and carefully paste the retrieved string. Once entered, proceed with the login process.

If the token is valid and hasn't expired, the Evento GUI will grant you access, transforming the login screen into a comprehensive dashboard displaying the inner workings of your distributed system. Here, you can leverage the various functionalities offered by the GUI, such as cluster visualization, telemetry monitoring, performance analysis, and flow visualization.

**Important Considerations:**

* **Token Expiration:** Be mindful that tokens typically have a limited lifespan. Once a token expires, it will no longer grant access, necessitating the retrieval of a new token from the application logs.
* **Security Best Practices:** While exploring the application logs for the token is a necessary step during the initial login, it's crucial to implement proper security measures once you're granted access. Consider utilizing a secure token management solution to generate, store, and rotate tokens for enhanced security.

By understanding the token-based authentication system and the process for obtaining a valid token, you'll be well-equipped to securely access and explore the powerful features of the Evento GUI. As you delve deeper into the framework, remember to prioritize security best practices to safeguard your distributed system.
