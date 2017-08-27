# AWS helloworld with Zappa

## Requirements

- Chalice (`pip install zappa`)
- The [credentials file](https://aws.amazon.com/es/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks/) already set up

## Steps

### Create the function in a file

Use your preferred WSGI framework and make sure that you expose a WSGI object (in this example, `app`):

```
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
    return jsonify(hello="world")

@app.route('/', methods=['POST'])
def greeting():
    body = request.get_json()
    message = 'Hello {} {}!'.format(body['first_name'], body['last_name'])
    return jsonify(message=message)
```

### Initialize the project

```
zappa init
```

Follow the instructions and answer the questions. Provide the `app` WSGI entrypoint in case it does not auto-detect it.

### Upload the function

```
zappa deploy
```

Take note of the endpoint url (`endpoint-url`)

### Test the funcion

```
curl -H "Content-Type: application/json" -X POST <endpoint-url> -d '{"first_name": "Margaret", "last_name": "Hamilton"}'
```
