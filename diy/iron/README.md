# Serverless helloworld with IronFunctions

## Requirements

- Install the `fn` CLI tools (run `curl -LSs https://goo.gl/VZrL8t | sh`)
- Run the `iron/functions` Docker container locally:

   ```
   docker run --rm -it --name functions -v ${PWD}/data:/app/data -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 iron/functions
   ```
- Alternative, you can also launch the UI:

  ```
  docker run --rm -it --link functions:api -p 4000:4000 -e "API_URL=http://api:8080" iron/functions-ui
  ```

## Steps

### Create a Docker container with your function

The specification says that the container expects its input via `stdin` and should return the results in `stdout`.

Thus, we can create `hello.py`:

```python
import os
import sys
import json

if not os.isatty(sys.stdin.fileno()):
    obj = json.loads(sys.stdin.read())
    first_name = obj.get("first_name")
    last_name = obj.get("last_name")
    message = 'Hello {} {}!'.format(first_name, last_name)

print(json.dumps({"message": message}))
```

We create a simple Dockerfile that runs this code, based on a slim image (`alpine3.6`):

```
FROM python:alpine3.6

WORKDIR /function
ADD . /function/
CMD ["python3", "hello.py"]
```

### Create the func.yml file

This file specifies the information about this function. The bare essentials are the version number and the Dockerhub repo where to push the resulting image:

```
name: lekum/hello
version: 1.0.0
```

### Build the container and push the image

Although it can be achieved with Docker commands, we can do it with `fn build && fn push`

### Create the app (helloapp) and a route to /hello

An app represents a group of related functions

```
fn apps create helloapp
```

We then map the path `/hello` to our function:

```
fn routes create helloapp /hello
```

### Test the app

```
curl localhost:8080/r/helloapp/hello -H "Content-Type: application/json" -X POST -d '{"first_name": "Margaret", "last_name": "Hamilton"}'
```
