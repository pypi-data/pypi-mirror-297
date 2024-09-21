from send_embed import send_embed
from send_message import send_message
def get_headers(auth_token):
    return {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }