from functools import reduce

from .enums import TextType
from .extractors import extract_markdown_images, extract_markdown_links
from .nodes import TextNode


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    if not isinstance(old_nodes, list):
        raise TypeError("Nodes must be a list of nodes.")
    return list(reduce(split_node_image, old_nodes, []))


def split_node_image(node_list: list[TextNode], node: TextNode):
    if not isinstance(node, TextNode):
        raise TypeError(f"Node is not a TextNode: {TextNode}")
    if node.text_type is not TextType.NORMAL:
        return node_list + [node]
    extracted_images = extract_markdown_images(node.text)
    if len(extracted_images) == 0:
        return node_list + [node]
    alt, url = extracted_images[0]
    before, after = node.text.split(f"![{alt}]({url})", maxsplit=1)
    before_nodes = [TextNode(before, TextType.NORMAL)] if before else []
    image_nodes = [TextNode(alt, TextType.IMAGE, url)]
    after_nodes = split_node_image(
        [],
        TextNode(after, TextType.NORMAL)
    ) if after else []
    return node_list + before_nodes + image_nodes + after_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes must be a list of TextNodes.")
    return list(reduce(split_node_link, old_nodes, []))


def split_node_link(node_list: list[TextNode], node: TextNode):
    if not isinstance(node, TextNode):
        raise TypeError("node must be a TextNode")
    if node.text_type is not TextType.NORMAL:
        return node_list + [node]
    extracted_links = extract_markdown_links(node.text)
    if len(extracted_links) == 0:
        return node_list + [node]
    text, url = extracted_links[0]
    before, after = node.text.split(f"[{text}]({url})", maxsplit=1)
    before_nodes = [TextNode(before, TextType.NORMAL)] if before else []
    link_nodes = [TextNode(text, TextType.LINK, url)]
    after_nodes = split_node_link(
        [],
        TextNode(after, TextType.NORMAL)
    ) if after else []
    return node_list + before_nodes + link_nodes + after_nodes
