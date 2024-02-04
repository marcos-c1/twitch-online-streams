import twitch
from models.user import User 

class UserController():
    def __init__(self):
        self.api = twitch.TwitchAPI()

    def get_user(self, login: str):
        payload = self.api.get_user(login)
        user_obj = User(payload)
        return user_obj
