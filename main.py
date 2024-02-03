from twitch import TwitchAPI

if __name__ == "__main__":
    api = TwitchAPI()
    #api.validate_token()
    api.get_followed_channels_live('rvlt1')
