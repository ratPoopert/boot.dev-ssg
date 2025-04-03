import re

from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType

from functools import reduce


def text_node_to_html_node(textnode: TextNode):
    match textnode.text_type:
        case TextType.NORMAL:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                None,
                {
                    "src": textnode.url,
                    "alt": textnode.text
                }
            )
        case _:
            raise TypeError("Unsupported text type")


def split_text_nodes_by_delimiter(
    textnodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
):
    def split_text_node_by_delimiter(
        textnodes: list[TextNode],
        textnode: TextNode
    ):
        if textnode.text.count(delimiter) % 2 != 0:
            raise ValueError("Missing matching delimiter.")
        if textnode.text_type != TextType.NORMAL:
            return textnodes + [textnode]
        split_text = textnode.text.split(delimiter)
        if textnode.text.startswith(delimiter):
            split_text.pop(0)
        if textnode.text.endswith(delimiter):
            split_text.pop(-1)
        new_nodes = []
        for i in range(0, len(split_text)):
            if textnode.text.startswith(delimiter):
                t = TextType.NORMAL if (i + 1) % 2 == 0 else text_type
            else:
                t = text_type if (i + 1) % 2 == 0 else TextType.NORMAL
            new_nodes.append(TextNode(split_text[i], t))
        return textnodes + new_nodes

    return list(reduce(
        split_text_node_by_delimiter,
        textnodes,
        [],
    ))


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    regexpr = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(regexpr, text)
    return result
