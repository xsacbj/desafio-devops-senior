from flask import Response
import json

def response(status, contentName, content, message=False):
    body = {}
    body[contentName] = content

    if(message):
        body["message"] = message

    return Response(json.dumps(body), status=status, mimetype='application/json')