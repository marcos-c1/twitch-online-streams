from models.channel import Channel
from twitch import TwitchAPI 

class ChannelController():
    def __init__(self):
        self.api = TwitchAPI()

    def get_followed_channels(self, user: str):
        payload = self.api.get_followed_channels_live(user)
        channels = []
        for i in range(len(payload)):
            ch = Channel(payload[i])
            channels.append(ch)
        return channels
