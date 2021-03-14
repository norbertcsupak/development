import json
import sys
import random
import requests
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' send messages')
    parser.add_argument('--message', required=True)
    args = parser.parse_args()
    url = "http://127.0.0.1:5000/api/webhook"
    message = (args.message)
    title = (f"New Incoming Message from norbert")
    hook_data = {
        "username": "NotificationBot",
        "icon_emoji": ":satellite:",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(hook_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(hook_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
