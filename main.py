from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from controllers.channel_controller import ChannelController 

# https://textual.textualize.io/
class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    #app = StopwatchApp()
    #app.run()
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

    #api.validate_token()
