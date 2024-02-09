class Channel:
    def __init__(self, payload):
        self.id = payload['id']
        self.user_id = payload['user_id']
        self.user_login = payload['user_login']
        self.user_name = payload['user_name']
        self.game_id = payload['game_id']
        self.game_name = payload['game_name']
        self.type = payload['type']
        self.title = payload['title']
        self.viewer_count = payload['viewer_count']
        self.started_at = payload['started_at']
        self.language = payload['language']
        self.thumbnail_url = payload['thumbnail_url']
        self.tag_ids = payload['tag_ids']
        self.tags = payload['tags']
        self.is_mature = payload['is_mature']
        self.payload = payload
        if 'pagination' in payload.keys():
            self.pagination = payload['pagination']

    def _get_payload(self) -> list:
        return self.payload
