import unittest

from ssg.nodes import TextNode
from ssg.enums import TextType


class TestTextNode(unittest.TestCase):
    def test__eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test__neq(self):
        control = TextNode("This is a text node", TextType.NORMAL)
        cases = (
            ("This is another text node", TextType.NORMAL),
            ("This is a text node", TextType.NORMAL, "https://www.google.com"),
            ("This is a text node", TextType.BOLD),
            ("This is a text node", TextType.ITALIC),
            ("This is a text node", TextType.CODE),
        )
        for case in cases:
            self.assertNotEqual(control, TextNode(*case))

    def test__repr(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        expected = "TextNode(This is a text node, Normal Text, None)"
        self.assertEqual(expected, repr(node))


if __name__ == "__main__":
    unittest.main()
