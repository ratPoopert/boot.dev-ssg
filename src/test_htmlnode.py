import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, None)
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

        node = HTMLNode(None, None, None, {})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

        node = HTMLNode(None, None, None, {
            "href": "https://www.google.com",
        })
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

        node = HTMLNode(None, None, None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        expected += ' target="_blank"'
        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
