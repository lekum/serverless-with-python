# Serverless with Python on Fission

## Requirements

Install `kubectl`, the `fission` cli and `minikube`

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.16.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
curl -Lo fission https://github.com/fission/fission/releases/download/nightly20170705/fission-cli-linux && chmod +x fission && sudo mv fission /usr/local/bin/
```

Start `minikube`:

```
minikube start
```

Launch Fission:

```
kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-rbac.yaml
kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-nodeport.yaml
```

Set the two environment variables `FISSION_URL` and `FISSION_ROUTER` as follows:

```
export FISSION_URL=http://$(minikube ip):31313
export FISSION_ROUTER=$(minikube ip):31314
```

## Steps

### Create a function handler

For example, this `hello.py`:

```python
import json
from flask import request

def main():
    data = json.loads(request.get_data().decode())
    message = 'Hello {} {}!'.format(data['first_name'], data['last_name'])
    return json.dumps({"message": message})
```

### Create the environment, the function and the route

```
fission env create --name python3 --image fission/python-env
fission function create --name hello --env python3 --code hello.py
fission route create --method POST --url /hello --function hello
```

### Test the function

```
curl -X POST -d '{"first_name": "Margaret", "last_name": "Hamilton"}' -H "Content-Type: application/json" http://$FISSION_ROUTER/hello
```
