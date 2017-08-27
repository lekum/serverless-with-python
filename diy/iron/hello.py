import os
import sys
import json

if not os.isatty(sys.stdin.fileno()):
    obj = json.loads(sys.stdin.read())
    first_name = obj.get("first_name")
    last_name = obj.get("last_name")
    message = 'Hello {} {}!'.format(first_name, last_name)

print(json.dumps({"message": message}))
