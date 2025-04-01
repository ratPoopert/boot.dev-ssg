import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test__props_to_html__returns_empty_string_on_none(self):
        node = HTMLNode(None, None, None, None)
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test__props_to_html__returns_empty_string_on_empty_dict(self):
        node = HTMLNode(None, None, None, {})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test__props_to_html__single_key_value_pair(self):
        node = HTMLNode(None, None, None, {
            "href": "https://www.google.com",
        })
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test__props_to_html__multiple_key_value_pairs(self):
        node = HTMLNode(None, None, None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
