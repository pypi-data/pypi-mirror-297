def get_headers(auth_token):
    return {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
