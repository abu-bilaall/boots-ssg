import unittest

from textnode import TextNode, TextType
from texttohtml import text_node_to_html_node
from htmlnode import LeafNode

class TestTextToHTML(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold_text(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)

    def test_italic_text(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_code_text(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, None)

    def test_link_text(self):
        node = TextNode("Click me", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image_alt_text(self):
        node = TextNode("Alt text", TextType.ALT, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})

    def test_link_without_url_raises_error(self):
        node = TextNode("Click me", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("URL is required for LINK", str(context.exception))

    def test_alt_without_url_raises_error(self):
        node = TextNode("Alt text", TextType.ALT)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("URL is required for ALT", str(context.exception))

    def test_invalid_text_type_raises_error(self):
        node = TextNode("Test", "invalid_type")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Invalid text_type", str(context.exception))

    def test_returns_leaf_node_instance(self):
        node = TextNode("Test", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)

    def test_empty_text_content(self):
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "b")

    def test_link_with_empty_url(self):
        node = TextNode("Click me", TextType.LINK, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_alt_with_empty_url(self):
        node = TextNode("Alt text", TextType.ALT, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)