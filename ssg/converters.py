import re

from .nodes import LeafNode, TextNode, HTMLNode, ParentNode
from .enums import BlockType, TextType
from .splitters import (
    split_text_nodes_by_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string.")
    root = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        root.children.append(_block_to_html_node(block))
    return root


def _block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return _paragraph_block_to_html_node(block)
        case BlockType.HEADING:
            return _heading_block_to_html_node(block)
        case BlockType.CODE:
            return _code_block_to_html_node(block)
        case BlockType.QUOTE:
            return _quote_block_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return _unordered_list_block_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return _ordered_list_block_to_html_node(block)
        case _:
            raise NotImplementedError("Unsupported block type")


def _paragraph_block_to_html_node(block: str) -> HTMLNode:
    child_nodes = map(text_node_to_html_node, text_to_textnodes(block))
    return ParentNode("p", list(child_nodes))


def _heading_block_to_html_node(block: str) -> HTMLNode:
    levels, text = block.split(" ", maxsplit=1)
    tag = f"h{len(levels)}"
    child_nodes = map(text_node_to_html_node, text_to_textnodes(text))
    return ParentNode(tag, list(child_nodes))


def _code_block_to_html_node(block: str) -> HTMLNode:
    text = block.strip("```\n").strip("\n```")
    text_node = TextNode(text, TextType.CODE)
    child_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [child_node])


def _quote_block_to_html_node(block: str) -> HTMLNode:
    text = " ".join(map(lambda line: line.lstrip("> "),
                        block.split("\n")))
    text_nodes = text_to_textnodes(text)
    child_nodes = map(text_node_to_html_node, text_nodes)
    return ParentNode("blockquote", list(child_nodes))


def _unordered_list_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode("ul",
                      _block_to_list_items(block))


def _ordered_list_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode("ol",
                      _block_to_list_items(block))


def _block_to_list_items(block: str) -> list[ParentNode]:
    lines = block.split("\n")
    return list(map(_line_to_list_item, lines))


def _line_to_list_item(line: str) -> ParentNode:
    prefix, text = line.split(" ", maxsplit=1)
    text_nodes = text_to_textnodes(text)
    child_nodes = map(text_node_to_html_node, text_nodes)
    return ParentNode("li", list(child_nodes))


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
                "",
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
    if _all_lines_start_with(">", block):
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
