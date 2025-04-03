from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(textnode: TextNode) -> LeafNode:
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
