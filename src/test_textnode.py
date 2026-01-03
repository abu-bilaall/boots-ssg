import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def setUp(self):
        self.bold_text = TextNode("This is a bold text node", TextType.BOLD)
        self.alt_text = TextNode("This is an alt text node", TextType.ALT)
        self.italic_text = TextNode("This is an italicized node", TextType.ITALIC)
        self.link_text = TextNode("This is a link node", TextType.LINK, "https://boot.dev/")
        self.link_text2 = TextNode("This is also a link node", TextType.LINK, "https://abubilaal.dev")
        self.undefined_link_text = TextNode("This is a link node", TextType.LINK)

    def test_eq(self):
        self.assertEqual(self.bold_text, self.bold_text)
    
    def test_not_eq(self):
        self.assertNotEqual(self.alt_text, self.italic_text)
    
    def test_url_type(self):
        self.assertNotEqual(self.link_text, self.link_text2)
    
    def test_url_edge(self):
        self.assertEqual(self.undefined_link_text, self.undefined_link_text)


if __name__ == "__main__":
    unittest.main()