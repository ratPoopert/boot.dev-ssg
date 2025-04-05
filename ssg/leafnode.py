from ssg.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf nodes must have a value.")
        if not self.tag:
            return self.value
        return "<{}{}>{}</{}>".format(
            self.tag,
            self.props_to_html(),
            self.value,
            self.tag,
        )
