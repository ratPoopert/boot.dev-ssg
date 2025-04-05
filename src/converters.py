from leafnode import LeafNode
from textnode import TextNode, TextType
from splitters import (
    split_text_nodes_by_delimiter,
    split_nodes_image,
    split_nodes_link,
)


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


def text_to_textnodes(text: str) -> list[TextNode]:
    if not isinstance(text, str):
        raise TypeError("text must be a string.")
    text_nodes = [TextNode(text, TextType.NORMAL)]
    extract_images = split_nodes_image(text_nodes)
    extract_links = split_nodes_link(extract_images)
    extract_bold = split_text_nodes_by_delimiter(extract_links,
                                                 "**",
                                                 TextType.BOLD)
    extract_italic = split_text_nodes_by_delimiter(extract_bold,
                                                   "_",
                                                   TextType.ITALIC)
    extract_code = split_text_nodes_by_delimiter(extract_italic,
                                                 "`",
                                                 TextType.CODE)
    return extract_code


def markdown_to_blocks(markdown: str) -> list[TextNode]:
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string.")
    split = markdown.split("\n\n")
    stripped = map(lambda s: s.strip(), split)
    filtered = filter(lambda s: s != "", stripped)
    return list(filtered)
