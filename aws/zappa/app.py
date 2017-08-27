from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
    return jsonify(hello="world")

@app.route('/', methods=['POST'])
def greeting():
    body = request.get_json()
    message = 'Hello {} {}!'.format(body['first_name'], body['last_name'])
    return jsonify(message=message)
