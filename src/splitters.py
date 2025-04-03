from functools import reduce

from textnode import TextNode, TextType


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
