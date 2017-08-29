# Serverless with Python on OpenFaas

## Requirements

Create a Swarm cluster of Ubuntu machines (you can try other distros but the commands here are for Ubuntu-like). If you want it locally, you can do it via [Vagrant](https://github.com/tdi/vagrant-docker-swarm) or you can use [play with Docker](http://labs.play-with-docker.com/).

## Steps

### Launch the OpenFaas stack

Log into a Swarm manager and run the following:

```
sudo apt-get install git && git clone https://github.com/alexellis/faas.git && cd faas && ./deploy_stack.sh
```

Install the `faas-cli` on the manager:

```
curl -sL https://cli.get-faas.com/ | sudo sh
```

### Create a handler function and a Dockerfile

Since Python3 is still not a valid template language for the platfor, we need to package our function in a Docker image and upload it to the Dockerhub.

For example, this could be our handler (`hello.py`):

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

And this could be the Dockerfile, taken from the example of Python 2 in the official [repo](https://github.com/alexellis/faas/blob/master/sample-functions/BaseFunctions/python/Dockerfile):

```
FROM python:3-alpine

ADD https://github.com/alexellis/faas/releases/download/0.5.1-alpha/fwatchdog /usr/bin
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /root/

COPY hello.py .

ENV fprocess="python3 hello.py"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
```

Then, we build and upload the image:

```
docker build -t lekum/faas-hello && docker push lekum/faas-hello
```

## Create the hello.yml

We then define the `hello.yml` as this:

```
provider:
  name: faas
  gateway: http://localhost:8080

functions:
  hello:
    image: lekum/faas-hello

```

And finally, upload it to the cluster:

```
faas-cli -action deploy -f ./hello.yml
```

## Test the function

You can go to the port 8080 of any member of the cluster and try invoking it on the web interface.

Otherwise, you can just run this from any node of the cluster:

```
curl localhost:8080/function/hello -H "Content-Type: application/json" -X POST -d '{"first_name": "Margaret", "last_name": "Hamilton"}'
```
