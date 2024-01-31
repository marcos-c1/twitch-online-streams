from os import path

def get_client_id():
    client_id = ""
    with open(path.expanduser('~/.twitch-client-id'), "r") as f:
        client_id = f.readline()[:-1]
    f.close()
    return client_id 

def get_client_secret():
    client_secret = ""
    with open(path.expanduser('~/.twitch-client-secret'), "r") as f:
        client_secret = f.readline()[:-1]        
    f.close()
    return client_secret 

def save_token(token: str):
    with open(path.expanduser('./token'), "w") as f:
        f.write(token)
    f.close()

