import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_is_htmlnode(self):
        node = LeafNode("p", "Hello world.")
        self.assertIsInstance(node, HTMLNode)

    def test_has_no_children(self):
        node = LeafNode("p", "Hello world.")
        self.assertIsNone(node.children)

    def test_requires_value(self):
        with self.assertRaises(TypeError):
            LeafNode("p")

    def test_requires_tag(self):
        with self.assertRaises(TypeError):
            LeafNode(value=None)

    def test_to_html(self):
        cases = (
            (
                LeafNode("p", "Hello world."),
                "<p>Hello world.</p>",
            ),
            (
                LeafNode("p", "Hello world.", {"class": "red"}),
                "<p class=\"red\">Hello world.</p>"
            ),
            (
                LeafNode(None, "Hello world.", {"class": "red"}),
                "Hello world."
            )
        )
        for node, expected in cases:
            self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
