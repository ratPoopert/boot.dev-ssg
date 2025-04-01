import unittest

from textnode import TextType, TextNode
from leafnode import LeafNode
from factories import (
    text_node_to_html_node,
    split_text_nodes_by_delimiter,
)


class TestFactories(unittest.TestCase):

    def test__text_node_to_html_node__no_text_type(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node(
                TextNode("Sample text", None)
            )

    def test__text_node_to_html_node__normal_text_type(self):
        text_node = TextNode("Sample text", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, text_node.text)

    def test__text_node_to_html_node__bold_text_type(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, text_node.text)

    def test__text_node_to_html_node__italic_text_type(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, text_node.text)

    def test__text_node_to_html_node__code_text_type(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, text_node.text)

    def test__text_node_to_html_node__link_text_type(self):
        text_node = TextNode("Link text",
                             TextType.LINK,
                             "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, text_node.text)
        self.assertEqual(html_node.props["href"],
                         text_node.url)

    def test__text_node_to_html_node__image_text_type(self):
        text_node = TextNode("Image text",
                             TextType.IMAGE,
                             "image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props["src"],
                         text_node.url)
        self.assertEqual(html_node.props["alt"],
                         text_node.text)

    def test__split_text_nodes_by_delimiter__unmatched_delimiter(self):
        with self.assertRaises(ValueError):
            split_text_nodes_by_delimiter(
                [
                    TextNode("Missing **delimiter", TextType.BOLD),
                ],
                "**",
                TextType.BOLD,
            )

    def test__split_text_nodes_by_delimiter__formatted_text_types(self):

        nodes = [
            TextNode("Bold node", TextType.BOLD),
            TextNode("Italic node", TextType.ITALIC),
            TextNode("Code node", TextType.CODE),
            TextNode("Image node", TextType.IMAGE, "image.png"),
            TextNode("Link node", TextType.LINK, "www.google.com"),
        ]
        self.assertEqual(
            nodes,
            split_text_nodes_by_delimiter(nodes, "**", TextType.BOLD)
        )

    def test__split_text_nodes_by_delimiter__normal_text(self):

        for text_type, d in (
            (TextType.BOLD, "**"),
            (TextType.ITALIC, "_"),
            (TextType.CODE, "`"),
        ):
            strings = [
                "This is normal text.",
                f"This has {d}special{d} text.",
                f"{d}This{d} delimiter is at the start.",
                f"This delimiter is at the {d}end.{d}",
                f"{d}This{d} has {d}two{d} delimiters.",
            ]
            nodes = list(map(lambda s: TextNode(s, TextType.NORMAL), strings))
            expected = [
                TextNode("This is normal text.", TextType.NORMAL),
                TextNode("This has ", TextType.NORMAL),
                TextNode("special", text_type),
                TextNode(" text.", TextType.NORMAL),
                TextNode("This", text_type),
                TextNode(" delimiter is at the start.", TextType.NORMAL),
                TextNode("This delimiter is at the ", TextType.NORMAL),
                TextNode("end.", text_type),
                TextNode("This", text_type),
                TextNode(" has ", TextType.NORMAL),
                TextNode("two", text_type),
                TextNode(" delimiters.", TextType.NORMAL),
            ]

            self.assertListEqual(
                split_text_nodes_by_delimiter(nodes, d, text_type),
                expected
            )


if __name__ == "__main__":
    unittest.main()
