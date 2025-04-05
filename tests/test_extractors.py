import unittest

from ssg.extractors import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
)


class TestExtractors(unittest.TestCase):

    def test__extract_markdown_images__takes_string(self):
        for invalid_type in [None, 1234, [], {}]:
            with self.assertRaises(TypeError):
                extract_markdown_images(invalid_type)

    def test__extract_markdown_images__returns_list_of_tuples(self):
        result = extract_markdown_images("This has an ![image](image.png)")
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, tuple)

    def test__extract_markdown_images__captures_alt_text(self):
        text = "This has an ![image](image.png)"
        result = extract_markdown_images(text)
        self.assertEqual("image", result[0][0])

    def test__extract_markdown_images__captures_image_url(self):
        text = "This has an ![image](image.png)"
        result = extract_markdown_images(text)
        self.assertEqual("image.png", result[0][1])

    def test__extract_markdown_images__captures_multiple_images(self):
        text = "This has ![an image](image1.png) and ![another image](image2.png)."
        result = extract_markdown_images(text)
        expected = [
            ("an image", "image1.png"),
            ("another image", "image2.png"),
        ]
        self.assertListEqual(result, expected)

    def test__extract_markdown_links__requires_string(self):
        for invalid_type in [None, 1234, 123.4, [], {}]:
            with self.assertRaises(TypeError):
                extract_markdown_links(invalid_type)

    def test__extract_markdown_links__returns_list_of_tuples(self):
        text = "This is a [link](www.google.com)"
        result = extract_markdown_links(text)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, tuple)

    def test__extract_markdown_links__captures_link_text(self):
        text = "This is a [link](www.google.com)"
        result = extract_markdown_links(text)
        self.assertEqual("link", result[0][0])

    def test__extract_markdown_links__captures_url(self):
        text = "This is a [link](www.google.com)"
        result = extract_markdown_links(text)
        self.assertEqual("www.google.com", result[0][1])

    def test__extract_markdown_links__captures_multiple_links(self):
        text = "This has [one link](google.com) and [another link](leidos.com)."
        result = extract_markdown_links(text)
        expected = [
            ("one link", "google.com"),
            ("another link", "leidos.com"),
        ]
        self.assertListEqual(result, expected)

    def test_extract_title(self):
        invalid_types = [1234, 123.4, [], {}, None]
        for t in invalid_types:
            with self.assertRaises(TypeError):
                extract_title(t)

        invalid_values = ["Has no heading", "# This has\n\n# Two headings"]
        for v in invalid_values:
            with self.assertRaises(ValueError):
                extract_title(v)

        for markdown, expected in (
            ("# Level 1 Heading", "Level 1 Heading"),
            ("# Document Title\n\nFirst paragraph", "Document Title"),
        ):
            self.assertEqual(extract_title(markdown), expected)


if __name__ == "__main__":
    unittest.main()
