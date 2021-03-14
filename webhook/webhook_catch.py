from flask import Flask, request, Response
#from urllib import unquote_plus
import json
import re

app = Flask(__name__)

@app.route('/api/webhook', methods=['POST'])
def respond():
    _msg=request.get_json()
    print(f'Message: {_msg["attachments"][0]["fields"]}')
    return Response(status=200)


def parse_request(req):
    """
    Parses application/json request body data into a Python dictionary
    """
    payload=request.get_json()
    return payload

@app.route('/api/print', methods=['POST'])
def print_test():
    """
    Send a POST request to localhost:5000/api/print with a JSON body with a "p" key
    to print that message in the server console.
    """
    payload = parse_request(request)
    print(payload)
    return ("", 200, None)
