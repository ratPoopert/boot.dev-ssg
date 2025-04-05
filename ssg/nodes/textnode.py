from ssg.enums import TextType


class TextNode:

    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: str = None
    ):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        return (
            self.text == o.text
            and self.text_type == o.text_type
            and self.url == o.url
        )

    def __repr__(self):
        return "TextNode({}, {}, {})".format(
            self.text,
            self.text_type.value,
            self.url,
        )
