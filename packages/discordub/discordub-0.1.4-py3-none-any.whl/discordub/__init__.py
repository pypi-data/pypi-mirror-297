import http.client
import json
import logging

def __init__(self, auth_token):
    self.headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    logging.basicConfig(level=logging.INFO)

def send_message(self, channel_id, content):
    try:
        conn = http.client.HTTPSConnection("discord.com")
        url = f"/api/v9/channels/{channel_id}/messages"
        payload = json.dumps({
            "content": content
        })
        conn.request("POST", url, body=payload, headers=self.headers)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            logging.info(f"Sent message: {content}")
        else:
            logging.error(f"Failed to send message: {res.status} - {data.decode('utf-8')}")
        conn.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def send_embed(self, channel_id, embed):
    try:
        conn = http.client.HTTPSConnection("discord.com")
        url = f"/api/v9/channels/{channel_id}/messages"
        payload = json.dumps({
            "embed": embed
        })
        conn.request("POST", url, body=payload, headers=self.headers)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            logging.info(f"Sent embed: {embed}")
        else:
            logging.error(f"Failed to send embed: {res.status} - {data.decode('utf-8')}")
        conn.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}")