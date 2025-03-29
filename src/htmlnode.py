from typing import Self


class HTMLNode:

    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list[Self] = None,
        props: dict[str, str] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ""
        if not isinstance(self.props, dict):
            return html
        for attr, val in self.props.items():
            html += f" {attr}=\"{val}\""
        return html
