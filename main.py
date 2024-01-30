import requests
import os

def get_client_secret():
    client_id = ""
    client_secret = ""
    with open(os.path.expanduser('~/.secret'), "r") as f:
        client_id = f.readline()
        client_secret = f.readline()        

    f.close()
    return client_id, client_secret 

def twitch_auth(client_id: str, client_secret: str):
    headers = dict()
    data = dict() 
    headers['content-type'] = 'application/x-www-form-urlencoded'
    data['client_id'] = client_id 
    data['client_secret'] = client_secret
    data['grant_type'] = 'client_credentials'

    response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=data).json()
    return response

if __name__ == '__main__':
    client_id, client_secret = get_client_secret()
    response = twitch_auth(client_id, client_secret)
    access_token = response["access_token"]
    print(access_token)
