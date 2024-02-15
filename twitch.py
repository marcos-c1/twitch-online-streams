from auth import Secret, Token 
from models.user import User 
from models.channel import Channel
from controllers.user_controller import UserController
import requests

# https://dev.twitch.tv/docs/api/reference/
class TwitchAPI():
    """
        Attributes:
            root_url: The root path to call all other endpoints in api
            client_id: The client id itself established
            token: The Token class object contain:
                user_token: Auth token returned by api in auth flow method
                refresh_token: Refresh token returned by api in case that user token expires
                expires_in: Remaining time to user token expires
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
        
    # GET 'https://id.twitch.tv/oauth2/validate'
    def get_current_user_id(self) -> str:
        """
            Example of response
            {
              "client_id": "wbmytr93xzw8zbg0p1izqyzzc5mbiz",
              "login": "twitchdev",
              "scopes": [
                "channel:read:subscriptions"
              ],
              "user_id": "141981764",
              "expires_in": 5520838
            }
                                                                                             
        """
        response = self.token.get_user_id_by_token()
        return response['user_id']
        
    # GET https://api.twitch.tv/helix/users?login=<username>
    # GET 'https://api.twitch.tv/helix/users?id=141981764'
    def get_user(self, user_id: str):
        url = ""
        if user_id:
            url = self.root_url + f'users?id={user_id}'
        else:
            raise Exception("No user_id parameter passed to get_user endpoint")
        
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
        token = self.token
        match response.status_code:
            case 200:
                try:
                    data = response.json()['data'][0]
                    """
                    user = User(payload)
                    self.user = user
                    """
                except Exception as e:
                    raise Exception(e)
                finally:
                    return response.json()['data'][0]
            case 401:
                token.refresh_user_token()
            case 500:
                raise Exception("Server error.") 
            case _:
                raise Exception(f"{response.status_code}: {response.content}")
        return None

    def get_followed_channels_live(self, user_id: str):
        client_id = self.client_id
        user_controller = UserController()
        user = user_controller.get_user(user_id)

        url = self.root_url + 'streams/followed' + f'?user_id={user.id}'
        
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

        response = requests.get(url, headers=headers)
        """
            Example of response
            {
              "data": [
                {
                  "id": "42170724654",
                  "user_id": "132954738",
                  "user_login": "aws",
                  "user_name": "AWS",
                  "game_id": "417752",
                  "game_name": "Talk Shows & Podcasts",
                  "type": "live",
                  "title": "AWS Howdy Partner! Y'all welcome ExtraHop to the show!",
                  "viewer_count": 20,
                  "started_at": "2021-03-31T20:57:26Z",
                  "language": "en",
                  "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_aws-{width}x{height}.jpg",
                  "tag_ids": [],
                  "tags": ["English"]
                },
                ...
              ],
              "pagination": {
                "cursor": "eyJiIjp7IkN1cnNvciI6ImV5SnpJam8zT0RNMk5TNDBORFF4TlRjMU1UY3hOU3dpWkNJNlptRnNjMlVzSW5RaU9uUnlkV1Y5In0sImEiOnsiQ3Vyc29yIjoiZXlKeklqb3hOVGs0TkM0MU56RXhNekExTVRZNU1ESXNJbVFpT21aaGJITmxMQ0owSWpwMGNuVmxmUT09In19"
              }
            }

        """
        token = self.token 
        match response.status_code:
            case 200:
                try:
                    channels = response.json()['data']
                    """
                    for i in range(len(channels)):
                        ch = Channel(channels[i])
                        print(f'{ch.user_name}')
                        print(f'{ch.title}')
                        print(f'{ch.game_name}')
                        print(f'{ch.viewer_count}')
                        print(f'{ch.started_at}')
                        print(f'{ch.language}')
                        print()
                    """
                except Exception as e:
                    raise Exception(e)
                finally:
                    return response.json()['data']
            case 401:
                """
                    401: Unauthorized

                    1. The ID in user_id must match the user ID found in the access token.
                    2. The Authorization header is required and must contain a user access token.
                    3. The user access token must include the user:read:follows scope.
                    4. The OAuth token is not valid.
                    5. The client ID specified in the Client-Id header does not match the client ID specified in the access token.

                """
                print(f"{response.status_code}: {response.content}")
                token.refresh_user_token()
            case 500:
                raise Exception("Server error.") 
            case _:
                raise Exception(f"{response.status_code}: {response.content}")
                print(response)
