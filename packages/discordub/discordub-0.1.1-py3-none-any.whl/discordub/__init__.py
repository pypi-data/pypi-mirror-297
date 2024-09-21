import http.client
import json

class Discordub:
    def __init__(self, auth_token):
        self.headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json"
        }

    def send_message(self, channel_id, content):
        conn = http.client.HTTPSConnection("discord.com")
        url = f"/api/v9/channels/{channel_id}/messages"
        payload = json.dumps({
            "content": content
        })
        conn.request("POST", url, body=payload, headers=self.headers)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            print(f"Sent message: {content}")
        else:
            print(f"Failed to send message: {res.status} - {data.decode('utf-8')}")
        conn.close()