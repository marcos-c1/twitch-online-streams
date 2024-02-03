class User():
    def __init__(self, payload):
        self.id = payload['id']
        self.login = payload['login']
        self.display_name = payload['display_name']
        self.type = payload['type']
        self.broadcaster_type = payload['broadcaster_type']
        self.description = payload['description']
        self.profile_image_url = payload['profile_image_url']
        self.offline_image_url = payload['offline_image_url']
        self.view_count = payload['view_count']
        self.created_at = payload['created_at']
