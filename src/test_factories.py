import unittest

from textnode import TextType, TextNode
from leafnode import LeafNode
from factories import (
    text_node_to_html_node,
    split_text_nodes_by_delimiter,
)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_raises_exception_on_unsupported_text_type(self):
        node = TextNode("Sample text", None)
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

    def test_returns_leaf_node(self):
        text_node = TextNode("Sample text", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)

    def test_normal_text_type(self):
        textnode = TextNode("Sample text", TextType.NORMAL)
        htmlnode = text_node_to_html_node(textnode)
        self.assertIsNone(htmlnode.tag)
        self.assertEqual(htmlnode.value, textnode.text)

    def test_bold_text_type(self):
        textnode = TextNode("Bold text", TextType.BOLD)
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.value, textnode.text)

    def test_italic_text_type(self):
        textnode = TextNode("Italic text", TextType.ITALIC)
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.tag, "i")
        self.assertEqual(htmlnode.value, textnode.text)

    def test_code_text_type(self):
        textnode = TextNode("Code text", TextType.CODE)
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.tag, "code")
        self.assertEqual(htmlnode.value, textnode.text)

    def test_link_text_type(self):
        textnode = TextNode("Link text",
                            TextType.LINK,
                            "https://www.google.com")
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.tag, "a")
        self.assertEqual(htmlnode.value, textnode.text)
        self.assertEqual(htmlnode.props["href"], textnode.url)

    def test_image_text_type(self):
        textnode = TextNode("Image text",
                            TextType.IMAGE,
                            "https://google.com/logo.png")
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.tag, "img")
        self.assertEqual(htmlnode.props["src"], textnode.url)
        self.assertEqual(htmlnode.props["alt"], textnode.text)


class TestSplitTextNodesByDelimiter(unittest.TestCase):

    def test_skips_non_text_types(self):
        textnodes = [
            TextNode("First node", TextType.BOLD),
            TextNode("Second node", TextType.ITALIC),
            TextNode("Third node", TextType.CODE),
            TextNode("Fourth node", TextType.IMAGE, "image.png"),
            TextNode("Fifth node", TextType.LINK, "www.google.com"),
        ]
        result = split_text_nodes_by_delimiter(
            textnodes,
            "**",
            TextType.BOLD,
        )
        self.assertListEqual(
            result,
            textnodes
        )

    def test_raises_exception_on_unmatched_delimiter(self):
        textnodes = [
            TextNode("Missing a **matching delimiter", TextType.NORMAL),
        ]
        with self.assertRaises(ValueError):
            split_text_nodes_by_delimiter(textnodes, "**", TextType.BOLD)

    def test_returns_correct_number_of_textnodes(self):
        cases = (
            (
                TextNode("This is sample text", TextType.NORMAL),
                1
            ),
            (
                TextNode("This is **sample** text", TextType.NORMAL),
                3
            ),
            (
                TextNode("**This** is **sample** text", TextType.NORMAL),
                4
            ),
        )
        for node, expected_count in cases:
            nodes = split_text_nodes_by_delimiter(
                [node],
                "**",
                TextType.BOLD,
            )
            self.assertEqual(len(nodes), expected_count)

    def test_handles_delimiters_mid_text(self):
        nodes = [TextNode("This has **bold** text.", TextType.NORMAL)]
        expected = [
            TextNode("This has ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.NORMAL),
        ]
        self.assertListEqual(
            split_text_nodes_by_delimiter(nodes, "**", TextType.BOLD),
            expected,
        )

    def test_handles_delimiter_at_start_of_text(self):
        nodes = [
            TextNode(
                "**This** delimiter is at the start.",
                TextType.NORMAL
            )
        ]
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" delimiter is at the start.", TextType.NORMAL),
        ]
        self.assertListEqual(
            split_text_nodes_by_delimiter(nodes, "**", TextType.BOLD),
            expected,
        )


if __name__ == "__main__":
    unittest.main()
