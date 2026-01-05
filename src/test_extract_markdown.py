import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "Here are images: ![one](https://example.com/1.png) and ![two](https://example.com/2.jpg)"
        matches = extract_markdown_images(text)
        expected = [("one", "https://example.com/1.png"), ("two", "https://example.com/2.jpg")]
        self.assertListEqual(matches, expected)

    def test_extract_image_with_empty_alt(self):
        text = "An image with empty alt: ![](https://example.com/image.png) end"
        matches = extract_markdown_images(text)
        expected = [("", "https://example.com/image.png")]
        self.assertListEqual(matches, expected)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(matches, expected)

    def test_extract_multiple_links(self):
        text = "Links: [one](https://one.example) [two](https://two.example)"
        matches = extract_markdown_links(text)
        expected = [("one", "https://one.example"), ("two", "https://two.example")]
        self.assertListEqual(matches, expected)

    def test_extract_empty_link_text(self):
        text = "A link with empty text: [](https://empty.example)"
        matches = extract_markdown_links(text)
        expected = [("", "https://empty.example")]
        self.assertListEqual(matches, expected)

    def test_links_do_not_match_images(self):
        text = "Image ![img](https://img.example) and a link [here](https://here.example)"
        matches = extract_markdown_links(text)
        expected = [("here", "https://here.example")]
        self.assertListEqual(matches, expected)