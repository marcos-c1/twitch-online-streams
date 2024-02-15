import twitch
from models.user import User 

class UserController():
    def __init__(self):
        self.api = twitch.TwitchAPI()

    def get_current_user_id(self) -> str:
        user = self.api.get_current_user_id()
        return user

    def get_user(self, user_id: str):
        payload = self.api.get_user(user_id)
        user_obj = User(payload)
        return user_obj
