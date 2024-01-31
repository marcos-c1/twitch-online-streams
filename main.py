import requests
from os import path
from utils import get_client_id, get_client_secret, save_token

def get_access_token():
    access_token = ""
    if(path.exists('./token')):
        with open(path.expanduser('./token'), "r") as f:
            access_token = f.readline()

    if not access_token:
        client_id = get_client_id() 
        client_secret = get_client_secret()
        response = twitch_auth_flow(client_id, client_secret)
        access_token = response["access_token"]
        return access_token
    return access_token

def twitch_auth_flow(client_id: str, client_secret: str):
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
    }

    response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=data).json()
    
    match response.status_code:
        case 200:
            try:
                save_token(response['access_token'])
            except e:
                raise Exception(e)
            finally:
                return response
        case 401:
            # TODO: Generate another access token and store.
            raise Exception("Token expired.")
        case 500:
            raise Exception("Server error.") 
        case _:
            raise Exception(f"{response.status_code}: {response.content}")

#def get_followed_channels_live():

def main():
    if __name__ == '__main__':
        access_token = get_access_token()
        print(access_token)

main()
