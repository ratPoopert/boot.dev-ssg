from functools import reduce
from .htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Unable to render HTML without tag.")
        start_tag = f"<{self.tag}{self.props_to_html()}>"
        end_tag = f"</{self.tag}>"
        return start_tag + self._inner_html() + end_tag

    def _inner_html(self):
        if self.children is None:
            raise ValueError("Unable to render inner HTML without children.")
        return reduce(
            lambda html, child: html + child.to_html(),
            self.children,
            ""
        )

    @staticmethod
    def child_to_html(html: str, child: HTMLNode):
        return html + child.to_html()
