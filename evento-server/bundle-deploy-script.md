---
description: Unveiling Evento Server's Bundle Deployment Script
---

# Bundle Deploy Script

In the intricate world of Evento-powered distributed systems, a crucial component operates behind the scenes, facilitating the seamless deployment of your applications. This chapter sheds light on the existence and functionality of the bundle deployment script, the silent maestro that manages the spawning of new bundle instances.

#### The Trigger: A Signal for Deployment

The exact trigger for invoking the bundle deployment script depends on your specific Evento framework implementation. It could be:

* **Manual deployment:** You might initiate deployment through a user interface or an API call within your Evento framework.
* **Event-driven deployment:** Certain events within your system, such as exceeding resource usage thresholds or triggering scaling policies, could prompt deployment of additional bundle instances.

Regardless of the trigger, the script is always called with two essential arguments:

* **JSON Encoded Bundle:** This argument carries the vital information about the bundle to be deployed. It's a JSON string representation of a complete `Bundle` object defined within your Evento framework code. This object encapsulates critical details like the bundle's ID, artifact location, environment variables, and more.

```json
{
  "id": "string",  // Unique identifier for the bundle
  "version": number,  // Version number of the bundle
  "description": "string",  // Optional description of the bundle
  "detail": "string",  // Optional additional details about the bundle
  "bucketType": "string",  // Type of bucket associated with the bundle (implementation specific)
  "artifactCoordinates": "string",  // Location of the bundle artifact (e.g., JAR file)
  "artifactOriginalName": "string",  // Original name of the bundle artifact
  "containsHandlers": boolean,  // Indicates if the bundle contains event handlers
  "environment": {
    "string": "string"  // Key-value pairs for environment variables
  },
  "vmOptions": {
    "string": "string"  // Key-value pairs for VM options (if applicable)
  },
  "autorun": boolean,  // Indicates if the bundle should be automatically run
  "minInstances": number,  // Minimum number of bundle instances to spawn (for scaling)
  "maxInstances": number,  // Maximum number of bundle instances to spawn (for scaling)
  "updatedAt": "string"  // Timestamp of the bundle's last update (in ISO 8601 format)
}
```

* **API Key:** The second argument serves as a security measure. It's an API key that grants temporary access to download the bundle artifact from the Evento Server. This mechanism ensures authorized access and prevents unauthorized deployments.

#### The Script in Action: Decoding and Orchestrating

Once triggered with the necessary arguments, the deployment script embarks on its mission:

1. **Parsing the Bundle Data:** The script utilizes the `json.loads` function to decipher the received JSON string. This transforms the string back into a Python dictionary, essentially reconstructing the `Bundle` object with all its properties.
2. **Extracting Bundle Details:** From the reconstructed `Bundle` object, the script meticulously extracts key information. This includes:
   * **Artifact Coordinates:** This property specifies the location of the bundle artifact, typically a JAR file containing the bundle's code and resources.
   * **Environment Variables:** These are custom configurations tailored for the specific bundle instance being deployed.
3. **Constructing the Docker Command:** Equipped with the extracted details, the script meticulously constructs a Docker run command. This command leverages the `docker run` subcommand to launch a new container that will house the deployed bundle.
   * **Unique Container Naming:** The container is assigned a unique name, often a combination of the bundle ID and a timestamp, guaranteeing no naming conflicts within the cluster.
   * **Specifying the Bundle Artifact:** The script utilizes the downloaded artifact URL (derived from the artifact coordinates) and the provided API key for authentication. This ensures the container has access to the necessary code to run the bundle.
   * **Environment Variable Injection:** Any environment variables defined within the bundle are meticulously added to the container using the `-e` flag. This provides the deployed bundle with its custom configuration.
   * **Container Image Selection:** Finally, the script specifies the container image to be used for running the bundle (likely named `evento-bundle-container`). This image contains the necessary runtime environment for your Evento bundles.
4. **Execution and Logging:** The script employs the `subprocess` module to execute the meticulously constructed Docker run command.
   * **Command Transparency:** Before execution, the script thoughtfully prints the entire command for debugging and logging purposes. This transparency allows for troubleshooting potential deployment issues.

#### The Provided Example: A Concrete Illustration

The provided code snippet showcases how the Docker run command gets constructed based on the extracted information from the bundle object. Let's dissect the example:

```python
import sys
import json
import subprocess
import time

print(sys.argv[1])
bundle = json.loads(sys.argv[1])
token = sys.argv[2]

print(bundle)

artifact = bundle["artifactCoordinates"]

print(artifact)

cmd = [
    "docker",
    "run",
    "--name", bundle["id"] + "-" + str(round(time.time() * 1000)),
    "-d",
    "--rm",
    "-e", "APP_JAR_URL=http://host.docker.internal:3000/asset/bundle/" + bundle["id"] + "?token=" + token]

for k, v in bundle["environment"]:
    cmd.append("-e")
    cmd.append(k + "=" + v)
cmd.append("evento-bundle-container")
print("Command: " + " ".join(cmd))
subprocess.run(cmd)

```

This constructed command essentially launches a new Docker container in detached mode (meaning it runs in the background) and removes itself upon termination. The container downloads the bundle artifact using the provided URL and API key, sets any environment variables, and finally executes the `evento-bundle-container` image, which presumably houses the runtime environment for your Evento bundles.

#### Conclusion:

The bundle deployment script serves as a crucial component within Evento Server, silently orchestrating the spawning of new bundle instances. By deciphering the JSON encoded bundle data and constructing appropriate Docker commands, the script ensures seamless
