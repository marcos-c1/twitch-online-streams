from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem, Static, Select
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.binding import Binding
from textual import on
from controllers.channel_controller import ChannelController 
from threading import Thread
from time import sleep

LIST_STREAM_CHANNELS = []
LIST_STREAM_CATEGORIES = []
DICT_STREAM = [] 

"""
dict keys:
    "id"
    "user_id"
    "user_login"
    "user_name"
    "game_id"
    "game_name"
    "type"
    "title"
    "viewer_count"
    "started_at"
    "language"
    "thumbnail_url"
"""

def append_to_list_from_set(s: set) -> None:
    for elem in s:
        LIST_STREAM_CATEGORIES.append(elem)

# https://textual.textualize.io/
class SelectCategories(Static):

    def compose(self) -> ComposeResult:
        yield Select((category, category) for category in LIST_STREAM_CATEGORIES)

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)

class ListStream(Static):

    def __init__(self):
        super().__init__()
        self.data = self._request_data() 
        channels = self.data 
        categories_set = set()
        for ch in channels:
            """
            dct_str['id'] = ch.id
            dct_str['user_id'] = ch.user_id
            dct_str['user_login'] = ch.user_login
            dct_str['user_name'] = ch.id
            dct_str['game_id'] = ch.id
            dct_str['game_name'] = ch.id
            dct_str['type'] = ch.id
            dct_str['title'] = ch.id
            dct_str['viewer_count'] = ch.id
            dct_str['started_at'] = ch.id
            dct_str['language'] = ch.id
            dct_str['thumbnail_url'] = ch.id
            dct_str['tag_ids'] = ch.id
            dct_str['tags'] = ch.id
            dct_str['is_mature'] = ch.id
           """ 
            DICT_STREAM.append(ch._get_payload())
            item = ListItem(Label(f"{ch.user_name}"))
            LIST_STREAM_CHANNELS.append(item)
            categories_set.add(f"{ch.game_name}")
        append_to_list_from_set(categories_set)
        #Thread(target=self._channels_loop, daemon=True).start()
                                               
    def _channels_loop(self) -> None:
         while True:
            self.data = self._request_data()
            self.update_channels()
            sleep(1000)

    def update_channels(self) -> None:
        channels = self.data
        for ch in channels:
            item = ListItem(Label(f"{ch.user_name}\n{ch.title}\n{ch.game_name}\n{ch.viewer_count}")),
            LIST_STREAM_CHANNELS.append(item)
        
    def _request_data(self): 
        ch_controller = ChannelController()
        channels = ch_controller.get_followed_channels('rvlt1')
        return channels

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield SelectCategories() 
        yield ListView(
            *LIST_STREAM_CHANNELS,
            id='list',
        )

class StreamApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "./css/app.tcss"

    BINDINGS = [
            ("d", "toggle_dark", "Toggle dark mode"),
            ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield ListStream()
        yield Footer()
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = StreamApp()
    app.run()
    """
    ch_controller = ChannelController()
    channels = ch_controller.get_followed_channels('rvlt1')
    
    for ch in channels:
        print(f'{ch.user_name}')
        print(f'{ch.title}')
        print(f'{ch.game_name}')
        print(f'{ch.viewer_count}')
        print(f'{ch.started_at}')
        print(f'{ch.language}')
        print()
    """
    #api.validate_token()
