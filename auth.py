from os import path
import requests

class Token():
    def __init__(self):
        self.path = './user_token'
        self.user_token = ""
        self.refresh_token = ""
        self.expires_in = 0

    def set_user_token(self):
        if(path.exists(self.path)):
            with open(path.expanduser(self.path), "r") as f:
                self.user_token = f.readline()[:-1]
                self.refresh_token = f.readline()[:-1]
                self.expires_in = f.readline()[:-1]
                                                                                                    
        if not self.user_token:
            return
                                                                                                    
    # TODO: Save scope aswell in future. 
    def save_user_token(self, token: str, refresh_token: str, expires_in: int):
        self.user_token = token
        self.refresh_token = refresh_token 
        self.expires_in = expires_in 
        with open(path.expanduser(self.path), "w") as f:
            f.write(f"{token}\n{refresh_token}\n{str(expires_in)}\n")
        f.close()

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
        self.__token = Token()
        self.__token.set_user_token()
        self.__client_id = Secret()._get_client_id()
        self.__client_secret = Secret()._get_client_secret()

    def _get_token(self):
        return self.__token 

    def _set_token(self, token: Token):
        self.__token = token

    def _get_client_id(self):
        return self.__client_id

    def _get_client_secret(self):
        return self.__client_secret

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
                    token = Token()
                    token.user_token = data['access_token']
                    token.refresh_token = data['refresh_token']
                    token.expires_in = data['expires_in']
                    self._set_token(token)
                    self._get_token().save_user_token(token.user_token, token.refresh_token, token.expires_in)
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
