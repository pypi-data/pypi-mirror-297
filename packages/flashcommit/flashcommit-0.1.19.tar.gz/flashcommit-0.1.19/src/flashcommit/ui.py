from typing import Type, Tuple

from rich.console import RenderableType
from textual import events
from textual._path import CSSPathType
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.driver import Driver
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.widgets import Static, Footer, Label, Button, TextArea

from flashcommit.flash_comit_adapter import FlashCommitAdapter


class Header(Static):
    comment = reactive("")

    def __init__(self, renderable: RenderableType = "", *, expand: bool = False, shrink: bool = False,
                 markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None,
                 disabled: bool = False) -> None:
        super().__init__(renderable, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes,
                         disabled=disabled)
        self.comment = renderable

    def watch_comment(self, comment: str) -> None:
        self.update(comment)


class QuitScreen(ModalScreen):
    """ https://www.blog.pythonlibrary.org/2024/02/06/creating-a-modal-dialog-for-your-tuis-in-textual/ """
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class ApplyScreen(Screen):

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None,
                 diff: str = None, header_text: str = None) -> None:
        super().__init__(name, id, classes)
        self.header_text = header_text
        self.diff = diff

    def compose(self) -> ComposeResult:
        yield Header(self.header_text, id="Header")
        yield Footer(id="Footer")
        editor = TextArea.code_editor(self.diff)
        editor.read_only = True
        yield editor


class LayoutApp(App):
    CSS_PATH = "console-ui.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="a",
            action="apply",
            description="Apply this patch",
        ),
        Binding(
            key="s",
            action="skip",
            description="Skip this patch",
        ),
        Binding(
            key="i",
            action="ignore",
            description="Ignore this patch",
        ),
    ]

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""
        self.push_screen(QuitScreen())

    def on_key(self, event: events.Key) -> None:
        if event.key == "a":
            self.fcommit.replace(self.get_file(), self.get_comment(), self.get_new_content())
            self.notify(
                self.get_header_text(),
                title="Successfully applied",
                severity="information",
            )
            self.next_step()
        if event.key == "s":
            self.fcommit.skip(*self.unpack())
            self.notify(
                self.get_header_text(),
                title="Skipped",
                severity="warning",
            )
            self.next_step()
        if event.key == "i":
            self.fcommit.ignore(*self.unpack())
            self.notify(
                self.get_header_text(),
                title="Ignored",
                severity="warning",
            )
            self.next_step()
        if event.key == "q":
            self.push_screen(QuitScreen())

    def next_step(self):
        if self.step_index + 1 >= len(self.review_steps):
            self.push_screen(QuitScreen())
        else:
            self.step_index = self.step_index + 1
            self.query("Header").last().comment = self.get_header_text()
            self.query("TextArea").last().text = self.get_diff()

    def get_header_text(self):
        if self.description is None:
            return f"'Change {self.step_index + 1}/{len(self.review_steps)}: {self.get_comment()}' in [i][b]{self.get_file()}[/b][/i]"
        else:
            return f"[b]{self.description}[/b]\nChange {self.step_index + 1}/{len(self.review_steps)}: '{self.get_comment()}' in [i][b]{self.get_file()}[/b][/i]"

    def get_diff(self):
        return self.fcommit.git_client.diff_file(self.get_file(), self.get_new_content())

    def get_new_content(self):
        return self.unpack()[2]

    def get_file(self):
        return self.unpack()[0]

    def get_comment(self):
        return self.unpack()[1]

    def __init__(self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None,
                 watch_css: bool = False,
                 fcommit: FlashCommitAdapter = None,
                 review_steps: list[Tuple[str, str, str]] = None, description: str = None) -> None:
        super().__init__(driver_class, css_path, watch_css)
        self.description = description
        self.review_steps = review_steps
        self.fcommit = fcommit
        self.step_index = 0

    def on_ready(self) -> None:
        self.push_screen(ApplyScreen(diff=self.get_diff(), header_text=self.get_header_text()))

    def unpack(self) -> tuple[str, str, str]:
        return (self.review_steps[self.step_index]["filename"],
                self.review_steps[self.step_index]["intention"],
                self.review_steps[self.step_index]["source"])


class UI:

    def __init__(self, fcommit: FlashCommitAdapter, review_steps: list[Tuple[str, str, str]], comments: str = None):
        super().__init__()
        self.app = LayoutApp(fcommit=fcommit, review_steps=review_steps, description=comments)

    def run(self):
        self.app.run()


def split_string(text, max_length=160):
    if len(text) <= max_length:
        return text, ""

    # Find the last space within the max_length
    split_index = text.rfind(' ', 0, max_length)

    if split_index == -1:
        # If no space is found, force split at max_length
        return text[:max_length], text[max_length:]
    else:
        return text[:split_index], text[split_index + 1:]
