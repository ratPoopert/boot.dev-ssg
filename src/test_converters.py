import unittest

from textnode import TextType, TextNode
from leafnode import LeafNode
from converters import (
    text_node_to_html_node,
    text_to_textnodes,
    markdown_to_blocks,
)


class TestConverters(unittest.TestCase):

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

    def test_text_to_textnodes(self):
        for invalid_input in [1234, 123.4, [], {}]:
            with self.assertRaises(TypeError):
                text_to_textnodes(invalid_input)
        text = " ".join([
            "Hello world!",
            "This has **bold text**.",
            "This has _italic text_.",
            "This has `some code`.",
            "This has ![an image](image.png).",
            "This has [a link](google.com).",
        ])
        result = text_to_textnodes(text)
        expected = [
            TextNode("Hello world! This has ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(". This has ", TextType.NORMAL),
            TextNode("italic text", TextType.ITALIC),
            TextNode(". This has ", TextType.NORMAL),
            TextNode("some code", TextType.CODE),
            TextNode(". This has ", TextType.NORMAL),
            TextNode("an image", TextType.IMAGE, "image.png"),
            TextNode(". This has ", TextType.NORMAL),
            TextNode("a link", TextType.LINK, "google.com"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(result, expected)

    def test_markdown_to_blocks(self):
        with self.assertRaises(TypeError):
            markdown_to_blocks(1234)

        markdown = """
This is just a block with a single sentence.

This is a second block.



There were extra lines between this block and the previous one.
This is a second sentence in the paragraph.
"""
        result = markdown_to_blocks(markdown)
        expected = [
            "This is just a block with a single sentence.",
            "This is a second block.",
            ("There were extra lines between this block and the previous one."
             "\nThis is a second sentence in the paragraph."),
        ]
        self.assertListEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
