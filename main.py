from twitch import TwitchAPI

if __name__ == "__main__":
    api = TwitchAPI()
    api.get_users_id('rvlt1')
