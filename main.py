from textual.app import App, ComposeResult
from PIL import Image
from typing import Any, Callable, ClassVar, Generic, Iterable, NamedTuple, TypeVar, cast
from textual import log 
from textual.widgets import Header, Footer, Label, ListView, ListItem, Static, Select, Log, DataTable, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.binding import Binding, BindingType
from textual import on
from textual.reactive import reactive
from controllers.channel_controller import ChannelController 
from controllers.user_controller import UserController
from models.user import User
from rich.text import Text, TextType
from threading import Thread
from time import sleep
from datetime import datetime
from zoneinfo import ZoneInfo
from textual_imageview.viewer import ImageViewer 

LIST_STREAM_CHANNELS = [
    ("User", "Title", "Category", "Uptime", "Views", "Language")
]
LIST_STREAM_CATEGORIES = []
LIST_STREAM_ITEMS = []
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

# https://textual.textualize.io/
class SelectCategories(Static):

    categories = set() 

    def __init__(self) -> None:
        super().__init__()
        self.user = self.__get_user()
        for row in LIST_STREAM_CHANNELS[1:]:
            self.categories.add(row[2])

    def __get_user(self) -> User:
        user_controller = UserController() 
        user_id = user_controller.get_current_user_id()
        user = user_controller.get_user(user_id)
        return user 

    def compose(self) -> ComposeResult:
        yield Select(((category, category) for category in self.categories), prompt="Select a category")
        yield Label(f"{self.user.display_name}")

class DataList(Static):

    BINDINGS: list[BindingType] = [
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("right", "cursor_right", "Cursor Right", show=False),
        Binding("left", "cursor_left", "Cursor Left", show=False),
        Binding("k", "page_up", "Page Up", show=False),
        Binding("j", "page_down", "Page Down", show=False),
    ]

    #Thread(target=self._channels_loop, daemon=True).start()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.BINDINGS = self.BINDINGS
        table.header_height = 2
        table.cursor_type = "row" 
        table.zebra_stripes = True
        table.add_columns(*LIST_STREAM_CHANNELS[0])
        for index, value in enumerate(LIST_STREAM_CHANNELS[1:]):
            table.add_row(*value, height=2, key=str(index))

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)
        table = self.query_one(DataTable)
        list_view = self.query_one(ListView)
        self.filter_category(table, self.title)
        self.filter_category_lv(list_view, self.title)
        table.refresh()

    def filter_category(self, table: DataTable, category: str):
        table.clear()
        for index, value in enumerate(LIST_STREAM_CHANNELS[1:]):
            if category == 'Select.BLANK': 
                table.add_row(*value, height=2, key=str(index))
            else:
                if value[2] == category:
                    table.add_row(*value, height=2, key=str(index))

    def filter_category_lv(self, list_view: ListView, category: str):
        list_view.clear()
        for i in range(1, len(LIST_STREAM_CHANNELS)):
            row = LIST_STREAM_CHANNELS[i]
            ITEM = ListItem(Label(f"{row[0]}\n{row[1]}\n{row[2]}\n{row[3]}\n{row[4]}\n{row[5]}"))
            if category == 'Select.BLANK':
                list_view.append(ITEM)
            else:
                if LIST_STREAM_CHANNELS[i][2] == category:
                    list_view.append(ITEM)
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        img = Image.open('./imgs/twitch-logo.png')
        yield SelectCategories() 
        with TabbedContent(initial="dt-tab"):
            with TabPane("Table", id="dt-tab"):  # First tab
                yield DataTable(
                    id='dt',
                )
            with TabPane("List", id="list-tab"):
                yield ListView(
                        *LIST_STREAM_ITEMS,
                )

class StreamApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "./css/app.tcss"

    BINDINGS = [
            ("d", "toggle_dark", "Toggle dark mode"),
            ("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        user_id = self._get_user_id()
        streams = self._get_followed_channels(user_id) 
                                                                                                          
        for ch in streams:
            """
            channel object attributes:
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
            #datetime_str = '09/19/22T13:55:26Z'
            diff_str = self.convert_utc_to_uptime(ch.started_at) 
            title = ch.title[:50] + '...' if len(ch.title) > 50 else ch.title
            #link_name = f'[link=https://www.twitch.tv/{ch.user_name}]{ch.user_name}[/link]'
            CHANNEL = (ch.user_name, title, ch.game_name, diff_str, ch.viewer_count, ch.language)
            ITEM = ListItem(Label(f"{ch.user_name}\n{title}\n{ch.game_name}\n{diff_str}\n{ch.viewer_count}\n{ch.language}"))
            LIST_STREAM_CHANNELS.append(CHANNEL)
            LIST_STREAM_ITEMS.append(ITEM)

    def convert_utc_to_uptime(self, utc: str) -> str:
        now_utc = datetime.now(ZoneInfo('UTC')).replace(tzinfo=None)
        started_at = datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
        diff = (now_utc - started_at)
        diff_str = ''.join(str(diff)).split('.')[0]
        return diff_str

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Vertical():
            yield DataList()
            yield Footer()
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def _get_followed_channels(self, user: str): 
        ch_controller = ChannelController()
        channels = ch_controller.get_followed_channels(user)
        return channels

    def _get_user_id(self) -> str:
        user_controller = UserController()
        user_id = user_controller.get_current_user_id()
        return user_id

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
