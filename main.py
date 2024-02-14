from textual.app import App, ComposeResult
from typing import Any, Callable, ClassVar, Generic, Iterable, NamedTuple, TypeVar, cast
from textual import log 
from textual.widgets import Header, Footer, Label, ListView, ListItem, Static, Select, Log, DataTable
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.binding import Binding, BindingType
from textual import on
from textual.reactive import reactive
from controllers.channel_controller import ChannelController 
from rich.text import Text, TextType
from threading import Thread
from time import sleep
from datetime import datetime
from zoneinfo import ZoneInfo

LIST_STREAM_CHANNELS = [
    ("User", "Title", "Category", "Uptime", "Views", "Language")
]
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

# https://textual.textualize.io/
class SelectCategories(Static):

    categories = set() 

    def __init__(self) -> None:
        super().__init__()
        for row in LIST_STREAM_CHANNELS:
            self.categories.add(row[2])

    def compose(self) -> ComposeResult:
        # TODO: Use the same object as DataTable use to filter by category
        """
            Probably will solve the problem
        """
        yield Select((category, category) for category in self.categories)

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
        self.filter_category(table, self.title)
        table.refresh()

    def filter_category(self, table: DataTable, category: str):
        table.clear()
        log(category)
        for index, value in enumerate(LIST_STREAM_CHANNELS[1:]):
            if category == 'Select.BLANK': 
                table.add_row(*value, height=2, key=str(index))
            else:
                if value[2] == category:
                    table.add_row(*value, height=2, key=str(index))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield SelectCategories() 
        yield DataTable(
            id='dt',
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
        streams = self._get_followed_channels() 
                                                                                                          
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
            now_utc = datetime.now(ZoneInfo('UTC')).replace(tzinfo=None)
            started_at = datetime.strptime(ch.started_at, "%Y-%m-%dT%H:%M:%SZ")
            diff = (now_utc - started_at)
            diff_str = ''.join(str(diff)).split('.')[0]
            CHANNEL = (ch.user_name, ch.title, ch.game_name, diff_str, ch.viewer_count, ch.language)
            LIST_STREAM_CHANNELS.append(CHANNEL)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Vertical():
            yield DataList()
            yield Footer()
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def _get_followed_channels(self): 
        ch_controller = ChannelController()
        channels = ch_controller.get_followed_channels('rvlt1')
        return channels

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
