from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem, Static
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.binding import Binding
from controllers.channel_controller import ChannelController 
from threading import Thread
from time import sleep

# https://textual.textualize.io/
class ListStream(Static):

    LIST_STREAM_CHANNELS = []
   
    def __init__(self):
        super().__init__()
        self.data = self._request_data() 
        channels = self.data 
        for index, ch in enumerate(channels):
            
            item = ListItem(Label(f"{ch.user_name}\n{ch.title}\n{ch.game_name}\n{ch.viewer_count}", id=f'label{i}'))
            self.LIST_STREAM_CHANNELS.append(item)
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
            self.LIST_STREAM_CHANNELS.append(item)
        
    def _request_data(self): 
        ch_controller = ChannelController()
        channels = ch_controller.get_followed_channels('rvlt1')
        return channels

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield ListView(
            *self.LIST_STREAM_CHANNELS,
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
