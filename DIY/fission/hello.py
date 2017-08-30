import json
from flask import request

def main():
    data = json.loads(request.get_data().decode())
    message = 'Hello {} {}!'.format(data['first_name'], data['last_name'])
    return json.dumps({"message": message})
