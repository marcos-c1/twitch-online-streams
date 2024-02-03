from auth import Secret, Token 
from models import user
import requests

# https://dev.twitch.tv/docs/api/reference/
class TwitchAPI():
    """
        Attributes:
            root_url: The root path to call all other endpoints in api
            client_id: The client id itself established
            token: The Token class object 
    """
    def __init__(self):
        self.root_url = 'https://api.twitch.tv/helix/'
        self.client_id = Secret()._get_client_id()
        token = Token()
        token.set_user_token()
        self.token = token
        self.user = None

    # GET 'https://id.twitch.tv/oauth2/validate'
    def validate_token(self):
        self.token.is_valid_token()
        
    # GET https://api.twitch.tv/helix/users?login=<username>
    # GET 'https://api.twitch.tv/helix/users?id=141981764'
    def get_users(self, login: str):
        url = self.root_url + f'users?login={login}'
        
        """
            Example of request
            curl -X GET 'https://api.twitch.tv/helix/users?id=141981764' \
            -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
            -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
        """
        headers = {
                'Authorization': f'Bearer {self.token.user_token}',
                'Client-Id': self.client_id
        }

        response = requests.get(url, headers=headers)
        """
            Example of response

            {'data': [
                {
                    'id': '79733625', 
                    'login': 'rvlt1', 
                    'display_name': 'rvlt1', 
                    'type': '', 
                    'broadcaster_type': '',
                    'description': '', 
                    'profile_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/bdf380b3-e9a6-4e20-ac1e-6e97ba153fe2-profile_image-300x300.png', 
                    'offline_image_url': '', 
                    'view_count': 0, 
                    'created_at': '2015-01-13T17:56:24Z'
                }
            ]}

        """
        match response.status_code:
            case 200:
                try:
                    data = response.json()
                    payload = data['data'][0]
                    user = User(payload)
                    self.user = user
                except e:
                    raise Exception(e)
                finally:
                    return response
            case 401:
                raise Exception("Token expired.")
            case 500:
                raise Exception("Server error.") 
            case _:
                raise Exception(f"{response.status_code}: {response.content}")
                print(response)

    def get_followed_channels_live(self, login: str):
        client_id = self.client_id
        user = self.user
        if not user:
            self.get_users(login)

        url = self.root_url + 'streams/followed' + f'?user_id={self.user.id}'
        
        """
            Example of request
            curl -X GET 'https://api.twitch.tv/helix/streams/followed?user_id=141981764' \
            -H 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx' \
            -H 'Client-Id: wbmytr93xzw8zbg0p1izqyzzc5mbiz'
        """

        headers = {
            'Authorization': f'Bearer {self.token.user_token}',
            'Client-Id': client_id 
        }
        params = {
                'user_id': client_id 
        }

        response = requests.get(url, params)
        
        match response.status_code:
            case 200:
                try:
                    data = response.json()
                    print(data)
                except e:
                    raise Exception(e)
                finally:
                    return response
            case 401:
                # TODO: Generate another access token and store.
                print(response.json())
                raise Exception("Token expired.")
            case 500:
                raise Exception("Server error.") 
            case _:
                raise Exception(f"{response.status_code}: {response.content}")
                print(response)
