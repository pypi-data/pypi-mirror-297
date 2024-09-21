import http.client
import json
import logging

logging.basicConfig(level=logging.INFO, format='[Discordbot] %(message)s')

def send_message(auth_token, channel_id, content):
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
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

def send_embed(auth_token, channel_id, embed):
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    try:
        conn = http.client.HTTPSConnection("discord.com")
        url = f"/api/v9/channels/{channel_id}/messages"
        payload = json.dumps({
            "embed": embed
        })
        conn.request("POST", url, body=payload, headers=headers)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            logging.info(f"Sent embed: {embed}")
        else:
            logging.error(f"Failed to send embed: {res.status} - {data.decode('utf-8')}")
        conn.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}")