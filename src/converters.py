from leafnode import LeafNode
from textnode import TextNode, TextType
from splitters import (
    split_text_nodes_by_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from blocks import BlockType
import re
from functools import reduce


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


def block_to_block_type(block: str) -> BlockType:
    if not isinstance(block, str):
        raise TypeError("Block must be a string.")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if _all_lines_start_with("> ", block):
        return BlockType.QUOTE
    if _all_lines_start_with("- ", block):
        return BlockType.UNORDERED_LIST
    if _is_ordered_list(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def _is_ordered_list(block: str):
    if not block.startswith("1. "):
        return False
    lines = block.split("\n")
    for i in range(0, len(lines)):
        line = lines[i]
        if not line.startswith(f"{i + 1}. "):
            return False
    return True


def _all_lines_start_with(prefix: str, block: str):
    lines = block.split("\n")
    matches = list(filter(lambda line: line.startswith(prefix), lines))
    return len(lines) == len(matches)
