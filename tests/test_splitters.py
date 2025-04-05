import unittest

from ssg.textnode import TextNode, TextType
from ssg.splitters import (
    split_text_nodes_by_delimiter,
    split_nodes_image,
    split_nodes_link,
)


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

    def test__split_nodes_image__takes_list_of_textnodes(self):
        invalid_inputs = [
            None,
            "",
            1234,
            {},
            [1234]
        ]
        for invalid_input in invalid_inputs:
            with self.assertRaises(TypeError):
                split_nodes_image(invalid_input)

    def test__split_nodes_image__returns_list_of_textnodes(self):
        node = TextNode("Just a simple node.", TextType.NORMAL)
        result = split_nodes_image([node])
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, TextNode)

    def test__split_nodes_image__no_change_when_image_is_not_present(self):
        text = "This node has no image."
        node = TextNode(text, TextType.NORMAL)
        result = split_nodes_image([node])
        self.assertListEqual(result, [node])

    def test__split_nodes_image__doesnt_modify_formatted_nodes(self):
        nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Code", TextType.CODE),
            TextNode("Image", TextType.IMAGE, "image.png"),
            TextNode("Link", TextType.LINK, "google.com"),
        ]
        result = split_nodes_image(nodes)
        self.assertListEqual(result, nodes)

    def test__split_nodes_image__converts_text_to_image(self):
        nodes = [TextNode("![Image Caption](image.png)", TextType.NORMAL)]
        result = split_nodes_image(nodes)
        expected = [TextNode("Image Caption", TextType.IMAGE, "image.png")]
        self.assertListEqual(result, expected)

    def test__split_nodes_image__handles_multiple_images_in_text(self):
        text = "![Image 1](image1.png) ![Image 2](image2.png) ![Image 3](image3.png)"
        nodes = [TextNode(text, TextType.NORMAL)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Image 1", TextType.IMAGE, "image1.png"),
            TextNode(" ", TextType.NORMAL),
            TextNode("Image 2", TextType.IMAGE, "image2.png"),
            TextNode(" ", TextType.NORMAL),
            TextNode("Image 3", TextType.IMAGE, "image3.png"),
        ]
        self.assertListEqual(result, expected)

    def test__split_nodes_image__handles_multiple_nodes(self):
        strings = [
            "This has ![one image](image.png)",
            "This has ![two](image1.png) ![images](image2.png)",
            "This image has no alt text ![](image.png)",
            "This ![image]() has no URL.",
        ]
        nodes = list(map(lambda s: TextNode(s, TextType.NORMAL), strings))
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This has ", TextType.NORMAL),
            TextNode("one image", TextType.IMAGE, "image.png"),
            TextNode("This has ", TextType.NORMAL),
            TextNode("two", TextType.IMAGE, "image1.png"),
            TextNode(" ", TextType.NORMAL),
            TextNode("images", TextType.IMAGE, "image2.png"),
            TextNode("This image has no alt text ", TextType.NORMAL),
            TextNode("", TextType.IMAGE, "image.png"),
            TextNode("This ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, ""),
            TextNode(" has no URL.", TextType.NORMAL),
        ]
        self.assertListEqual(result, expected)

    def test_split_nodes_link(self):
        for invalid_input in ["", 1234, 123.4, {}, [""]]:
            with self.assertRaises(TypeError):
                split_nodes_link(invalid_input)

        skipped_nodes = [
            TextNode("Hello BOLD", TextType.BOLD),
            TextNode("Hello ITALIC", TextType.ITALIC),
            TextNode("Hello CODE", TextType.CODE),
            TextNode("Hello IMAGE", TextType.IMAGE, "image.png"),
            TextNode("Hello LINK", TextType.LINK, "google.com"),
        ]
        nodes = list(map(lambda s: TextNode(s, TextType.NORMAL), [
            "Just a string",
            "[Hello LINK](url.com)",
            "[First LINK](url.com) [Second LINK](url.com)",
            "Some text [with](url.com) a link",
            "[No URL]()",
            "[](notext.com)"
        ]))
        result = split_nodes_link(skipped_nodes + nodes)
        expected = skipped_nodes + [
            TextNode("Just a string", TextType.NORMAL),
            TextNode("Hello LINK", TextType.LINK, "url.com"),
            TextNode("First LINK", TextType.LINK, "url.com"),
            TextNode(" ", TextType.NORMAL),
            TextNode("Second LINK", TextType.LINK, "url.com"),
            TextNode("Some text ", TextType.NORMAL),
            TextNode("with", TextType.LINK, "url.com"),
            TextNode(" a link", TextType.NORMAL),
            TextNode("No URL", TextType.LINK, ""),
            TextNode("", TextType.LINK, "notext.com"),
        ]
        self.assertListEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
