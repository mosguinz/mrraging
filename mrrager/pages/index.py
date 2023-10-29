"""The home page of the app."""

from mrrager import styles
from mrrager.templates import template
from mrrager.components import cam_stream
from mrrager.background import emotion_scan

import reflex as rx


@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return rx.vstack(
        cam_stream.camera(),
        rx.text(
            "Emotions: ",
            emotion_scan.EmotionScan.emotions,
            on_click=emotion_scan.EmotionScan.update_emotions,
        ),
    )
