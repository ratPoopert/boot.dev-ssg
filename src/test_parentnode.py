import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_tag_required(self):
        with self.assertRaises(TypeError):
            ParentNode(children=None)

    def test_children_required(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="p")

    def test_has_no_value(self):
        node = ParentNode("p", None)
        self.assertIsNone(node.value)

    def test_props_are_optional(self):
        node = ParentNode("p", None)
        self.assertIsNone(node.props)

    def test_to_html_requires_tag(self):
        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_requires_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_returns_string(self):
        node = ParentNode("p", [])
        self.assertIsInstance(node.to_html(), str)

    def test_to_html_recurses_over_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode("div", [
                    LeafNode(None, "Nested text"),
                ]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            (
                "<p>"
                "<b>Bold text</b>"
                "Normal text"
                "<i>italic text</i>"
                "Normal text"
                "<div>Nested text</div>"
                "</p>"
            )
        )


if __name__ == "__main__":
    unittest.main()
