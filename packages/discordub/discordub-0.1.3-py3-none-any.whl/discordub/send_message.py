import http.client
import json
import logging
from __init__ import get_headers

logging.basicConfig(level=logging.INFO)

def send_message(auth_token, channel_id, content):
    headers = get_headers(auth_token)
    try:
        conn = http.client.HTTPSConnection("discord.com")
        url = f"/api/v9/channels/{channel_id}/messages"
        payload = json.dumps({
            "content": content
        })
        conn.request("POST", url, body=payload, headers=headers)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            logging.info(f"Sent message: {content}")
        else:
            logging.error(f"Failed to send message: {res.status} - {data.decode('utf-8')}")
        conn.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
