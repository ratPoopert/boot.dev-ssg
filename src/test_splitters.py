import unittest

from textnode import TextNode, TextType
from splitters import split_text_nodes_by_delimiter


class TestSplitters(unittest.TestCase):

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
