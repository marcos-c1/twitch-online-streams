from auth import Secret, Token 
import requests

# https://dev.twitch.tv/docs/api/reference/

class TwitchAPI():
    def __init__(self):
        self.root_url = 'https://api.twitch.tv/helix/'
        self.client_id = Secret()._get_client_id()
        token = Token()
        token.set_user_token()
        self.user_token = token.user_token 

    # GET https://api.twitch.tv/helix/users?login=<username>
    # GET 'https://api.twitch.tv/helix/users?id=141981764'
    def get_users_id(self, login: str):
        url = self.root_url + f'users?login={login}'
        
        """
            Example of request
            curl -X GET 'https://api.twitch.tv/helix/users?id=141981764' \
            -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
            -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
        """
        headers = {
                'Authorization': f'Bearer {self.user_token}',
                'Client-Id': self.client_id
        }

        response = requests.get(url, headers=headers)
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
                raise Exception("Token expired.")
            case 500:
                raise Exception("Server error.") 
            case _:
                raise Exception(f"{response.status_code}: {response.content}")
                print(response)

    def get_followed_channels_live(self):
        url = self.root_url + 'streams/followed'
        
        """
            Example of request
            curl -X GET 'https://api.twitch.tv/helix/streams/followed?user_id=141981764' \
            -H 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx' \
            -H 'Client-Id: wbmytr93xzw8zbg0p1izqyzzc5mbiz'
        """

        headers = {
            'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx'
        }
        params = {
                'user_id': self.client_id 
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
                raise Exception("Token expired.")
            case 500:
                raise Exception("Server error.") 
            case _:
                raise Exception(f"{response.status_code}: {response.content}")
                print(response)
