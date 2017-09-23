# Serverless with Python on OpenFaas

![Project Logo](https://camo.githubusercontent.com/cf01eefb5b6905f3774376d6d1ed55b8f052d211/68747470733a2f2f626c6f672e616c6578656c6c69732e696f2f636f6e74656e742f696d616765732f323031372f30382f666161735f736964652e706e67)

Website: https://www.openfaas.com

## Requirements

Create a Swarm cluster of Ubuntu machines (you can try other distros but the commands here are for Ubuntu-like). If you want it locally, you can do it via [Vagrant](https://github.com/tdi/vagrant-docker-swarm) or you can use [play with Docker](http://labs.play-with-docker.com/).

## Steps

### Launch the OpenFaas stack

Log into a Swarm manager and run the following:

```
sudo apt-get install git \
  && git clone https://github.com/alexellis/faas.git \
  && cd faas && ./deploy_stack.sh
```

Install the `faas-cli` on the manager:

```
curl -sL https://cli.openfaas.com/ | sudo sh
```

### Create a handler function and a Dockerfile

There is an official language template for Python2.7, but since we want to use Python3 we'll set the language to "Dockerfile" and this lets us use a custom Dockerfile.

For example, this could be our handler (`main.py`):

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

The Dockerfile is in the handler folder:

```
FROM python:3-alpine

ADD https://github.com/alexellis/faas/releases/download/0.6.5/fwatchdog /usr/bin
RUN chmod +x /usr/bin/fwatchdog

WORKDIR /root/

COPY main.py .

ENV fprocess="python3 main.py"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
```

> To generate these files for Python 2.7 type in `faas-cli new --lang python --name myfunction`. This step generates your handler.py, requirements.txt and YAML file automatically.


## Create the hello.yml

We then define the `hello.yml` as this:

```
provider:
  name: faas
  gateway: http://localhost:8080

functions:
  hello:
    lang: Dockerfile
    handler: ./handler
    image: lekum/faas-hello
```

Now we use the CLI to build/push and deploy:

```
faas-cli build -f hello.yml
```

> If you have more than one function you can pass in `--parallel=4` to build in parallel or `--squash` to produce an image with fewer layers.

```
faas-cli push -f hello.yml
```

We only need to push the image if we have a multi-node or remote cluster.

```
faas-cli deploy -f hello.yml
```

## Invoke the function

Use the CLI to invoke the function or list them:

```
faas-cli list -f hello.yml
Function                        Invocations     Replicas
func_webhookstash               0               1
func_decodebase64               0               1
hello                           7               1
func_hubstats                   0               1
func_nodeinfo                   0               1
func_base64                     0               1
func_markdown                   0               1
func_echoit                     0               1
func_wordcount                  0               1
```

> You can also see the sample functions available in the stack.

And:

```
echo '{"first_name": "Margaret", "last_name": "Hamilton"}' | faas-cli invoke --name hello
{"message": "Hello Margaret Hamilton!"}

```

Alternatively: you can go to the port 8080 of any member of the cluster and try invoking it on the web interface.

http://localhost:8080/

![Portal UI](https://user-images.githubusercontent.com/6358735/30772105-f0e599b4-a04c-11e7-9728-922240cb76b8.png)

Otherwise, you can just run this from any node of the cluster:

```
curl localhost:8080/function/hello -H "Content-Type: application/json" -X POST -d '{"first_name": "Margaret", "last_name": "Hamilton"}'
```

Prometheus metrics are built-in and available on http://localhost:9090/

A good query is `rate(gateway_function_invocation_total[20s])` - then click "Graph"

Prometheus metrics are also used for auto-scaling your functions. You can find out more on the OpenFaaS repo - https://github.com/alexellis/faas/