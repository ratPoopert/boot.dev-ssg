from typing import Self


class HTMLNode:

    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list[Self] = None,
        props: dict[str, str] = None,
    ):
        if not isinstance(tag, (str, type(None))):
            raise TypeError("Tag must be a string")
        if not isinstance(value, (str, type(None))):
            raise TypeError("Value must be a string")
        if not isinstance(children, (list, type(None))):
            raise TypeError("Children must be a list of HTMLNodes")
        if not isinstance(props, (dict, type(None))):
            raise TypeError(
                "Props must be a dictionary of attributes and values")
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
