# Serverless with Python on OpenWhisk

## Requirements

### Install the OpenWhisk Vagrant box

```
git clone --depth=1 https://github.com/apache/incubator-openwhisk.git openwhisk
cd openwhisk/tools/vagrant
./hello
```

## Steps

### Enter the VirtualBox machine

```
vagrant ssh
```

### Create the function in hello.py

```python
def main(args):
    first_name = args.get("first_name")
    last_name = args.get("last_name")
    message = 'Hello {} {}!'.format(first_name, last_name)
    return {"message": message}
```

### Upload the function

```
wsk action create hello hello.py --kind python:3
```

### Invoke the function via wsk cli

```
wsk action invoke hello --param first_name Margaret --param last_name Hamilton --result
```

### Invoke the function via HTTP

Not so simple. First, get the `url` of the function:

```
wsk action get hello --url
```

Get the basic authentication base64 hash (`basic-auth`) running:

```
wsk namespace list -v
```

Now you can test it:

```
curl <url>?blocking=true -X POST -H "Content-Type: application/json" -d '{"first_name": "Margaret", "last_name": "Hamilton"}' -k -H "Authorization:Basic <basic-auth>"
```
