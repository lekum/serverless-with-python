# AWS helloworld with Chalice

## Requirements

- Chalice (`pip install chalice`)
- The [credentials](http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html) already set up

## Steps

### Initialize the project

```
chalice new-project helloworld && cd helloworld
```

### Modify the app.py file

For example, for our `helloworld`:

```
from chalice import Chalice

app = Chalice(app_name='helloworld')


@app.route('/', methods=['POST'])
def greeting():
    body = app.current_request.json_body
    message = 'Hello {} {}!'.format(body['first_name'], body['last_name'])
    return { "message" : message }
```

### Upload the function

```
chalice deploy
```

Take note of the endpoint url (`endpoint-url`)

### Test the funcion

```
curl -H "Content-Type: application/json" -X POST <endpoint-url> -d '{"first_name": "Margaret", "last_name": "Hamilton"}'
```
