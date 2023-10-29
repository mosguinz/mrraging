"""The home page of the app."""

from mrrager import styles
from mrrager.templates import template
from mrrager.components import cam_stream

import reflex as rx


@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return cam_stream.camera()

    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()

    return rx.markdown(content, component_map=styles.markdown_style)
