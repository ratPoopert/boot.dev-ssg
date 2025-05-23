import unittest

from ssg.nodes import TextNode, LeafNode, ParentNode
from ssg.converters import (
    markdown_to_html_node,
    text_node_to_html_node,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
)
from ssg.enums import BlockType, TextType


class TestConverters(unittest.TestCase):

    def test_markdown_to_html_node(self):
        for invalid_arg in [1234, 123.4, [], {}, None]:
            with self.assertRaises(TypeError):
                markdown_to_html_node(invalid_arg)

        markdown = """
# Heading 1

This is a paragraph. It has **bold text**, _italic text_, and `code`.

This paragraph has [a link](google.com).

This paragraph has ![an image](image.png).

```
if code:
    return False
```

> This is a quote.
> Cite me please.

- Item
- Another item

1. Item 1
2. Item 2
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Heading 1</h1>"
            "<p>This is a paragraph. It has <b>bold text</b>, <i>italic text</i>, and <code>code</code>.</p>"
            "<p>This paragraph has <a href=\"google.com\">a link</a>.</p>"
            "<p>This paragraph has <img src=\"image.png\" alt=\"an image\"></img>.</p>"
            "<pre><code>if code:\n    return False</code></pre>"
            "<blockquote>This is a quote. Cite me please.</blockquote>"
            "<ul><li>Item</li><li>Another item</li></ul>"
            "<ol><li>Item 1</li><li>Item 2</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

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
        self.assertEqual(html_node.value, "")
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

    def test_block_to_block_type(self):
        with self.assertRaises(TypeError):
            block_to_block_type(None)

        cases = (
            (
                "This is a paragraph.\nThere's nothing special about it.",
                BlockType.PARAGRAPH,
            ),
            ("#Not a heading", BlockType.PARAGRAPH),
            ("# Heading 1", BlockType.HEADING),
            ("###### Heading 6", BlockType.HEADING),
            ("####### Too many levels", BlockType.PARAGRAPH),
            ("```\nSome code\n```", BlockType.CODE),
            ("> This\n> is a\n> blockquote", BlockType.QUOTE),
            ("> This is\nnot a blockquote", BlockType.PARAGRAPH),
            ("- List item 1\n- List item 2", BlockType.UNORDERED_LIST),
            ("1. List item 1\n2. List item 2", BlockType.ORDERED_LIST),
            ("2. List item 1\n1. List item 2", BlockType.PARAGRAPH),
        )
        for block, expected in cases:
            self.assertEqual(block_to_block_type(block), expected)


if __name__ == "__main__":
    unittest.main()
