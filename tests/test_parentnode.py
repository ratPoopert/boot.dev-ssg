import unittest

from ssg.parentnode import ParentNode
from ssg.leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test__init__requires_tag(self):
        with self.assertRaises(TypeError):
            ParentNode(children=None)

    def test__init__requires_children(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="p")

    def test__init__value_is_none(self):
        node = ParentNode("p", None)
        self.assertIsNone(node.value)

    def test__init__props_are_optional(self):
        node = ParentNode("p", None)
        self.assertIsNone(node.props)

    def test__to_html__requires_tag(self):
        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test__to_html__requires_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test__to_html__returns_string(self):
        node = ParentNode("p", [])
        self.assertIsInstance(node.to_html(), str)

    def test__to_html__recurses_over_children(self):
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
