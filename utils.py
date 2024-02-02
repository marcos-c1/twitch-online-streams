from os import path
import requests

class Secret():
    def __init__(self, path_id=".twitch-client-id", path_secret=".twitch-client-secret"):
        self.path_id = path_id
        self.path_secret = path_secret
        self.client_id = ""
        self.client_secret = ""

    def _get_client_id(self):
        if not self.client_id:
            with open(path.expanduser('.twitch-client-id'), "r") as f:
                self.client_id = f.readline()[:-1]
            f.close()
        return self.client_id 
                                                                         
    def _get_client_secret(self):
        if not self.client_secret: 
            with open(path.expanduser('.twitch-client-secret'), "r") as f:
                self.client_secret = f.readline()[:-1]        
            f.close()
        return self.client_secret 
                                                                     
class OAuth():
    def __init__(self):
        secret = Secret()
        self.__client_id = secret._get_client_id()
        self.__client_secret = secret._get_client_secret()

    def _get_client_id(self):
        return self.__client_id

    def _get_client_secret(self):
        return self.__client_secret

    def get_user_token():
        access_token = ""
        if(path.exists('./user_token')):
            with open(path.expanduser('./user_token'), "r") as f:
                user_token = f.readline()[:-1]
                refresh_token = f.readline()[:-1]
                expires_in = f.readline()[:-1]

        if not user_token:
            raise Exception("There isnt a user token saved. Please authorize your twitch account.")
        return user_token, refresh_token, expires_in 

    def save_user_token(token: str, refresh_token: str, expires_in: int):
        with open(path.expanduser('./user_token'), "w") as f:
            f.write(f"{token}\n{refresh_token}\n{str(expires_in)}\n")
        f.close()

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def set_query_params(self, scope: str, response_type="code"):
        client_id = self._get_client_id()
        redirect_uri = "http://localhost:3000"
        self.query = f'response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'

    def get_query_params(self):
        return self.query

    def twitch_auth_flow(self):
        client_id = self._get_client_id()
        client_secret = self._get_client_secret()
        code = self.code

        headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
                'client_id': client_id, 
                'client_secret': client_secret, 
                'code': code, 
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:3000'
        }

        response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=data)
        
        """
            If success, returns this as result.
        {
          "access_token": "rfx2uswqe8l4g1mkagrvg5tv0ks3",
          "expires_in": 14124,
          "refresh_token": "5b93chm6hdve3mycz05zfzatkfdenfspp1h1ar2xxdalen01",
          "scope": [
            "channel:moderate",
            "chat:edit",
            "chat:read"
          ],
          "token_type": "bearer"
        }

        """

        match response.status_code:
            case 200:
                try:
                    data = response.json()
                    print(data)
                    self.access_token = data['access_token']
                    self.refresh_token = data['refresh_token']
                    self.expires_in = data['expires_in']
                    save_user_token(self.access_token, self.refresh_token, self.expires_in)
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
