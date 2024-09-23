import asyncio
import itertools

from textual import work
from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Label
from textual.widgets import Markdown


class MyApp(App):
    """A Textual app to monitor and command the PLATO F-FEE."""

    DEFAULT_CSS = """
    Label {
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding(key="f1", action="help", description="Help", show=True, priority=True),
    ]

    def __init__(self):
        super().__init__()
        self._poll_timer = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        with Vertical():
            yield Label("Hello, World!", id="lbl-hello")

    def on_mount(self):
        self._poll_timer = self.set_timer(1.0, self.poll_services)

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen())

    @work()
    async def poll_services(self):
        names = itertools.cycle(["John", "Bart", "melissa", "Kris"])

        while True:
            await asyncio.sleep(2.0)
            self.query_one("#lbl-hello", Label).update(f"Hello, {next(names)}!")


HELP = """
# A Simple Help Modal Screen.

This is an example App tp serve as a MRE.
Use ESCAPE to dismiss.
"""


class HelpScreen(ModalScreen[None]):
    """Modal dialog that shows the application's help."""

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    HelpScreen > Vertical {
        border: thick grey 50%;
        width: 60%;
        height: 80%;
        background: $boost;
    }

    """

    BINDINGS = [Binding("escape", "dismiss", "", show=False)]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Markdown(HELP)

    def action_dismiss(self, result=None):
        self.dismiss(result)


if __name__ == '__main__':
    app = MyApp()
    app.run()
