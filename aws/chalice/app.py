from chalice import Chalice

app = Chalice(app_name='helloworld')


@app.route('/', methods=['POST'])
def greeting():
    body = app.current_request.json_body
    message = 'Hello {} {}!'.format(body['first_name'], body['last_name'])
    return { "message" : message }
