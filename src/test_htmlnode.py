import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.link_node = HTMLNode(tag="a", value="click me", props={"href":"https://www.google.com", "target":"_blank"})
        self.empty_node = HTMLNode()
        self.title_node = HTMLNode(tag="title", value="Document")
        self.head_node = HTMLNode(tag="head", children=[self.title_node])
    
    def test_repr(self):
        output = self.link_node.__repr__()
        expected = 'HTMLNode(tag: a, value: click me, children: None, attributes: href="https://www.google.com" target="_blank")'
        self.assertEqual(output, expected)
    
    def test_props_to_html(self):
        attributes = self.link_node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(attributes, expected)
    
    def test_children_to_string(self):
        output = self.head_node.children_to_string()
        expected = 'HTMLNode(tag: title, value: Document, children: None, attributes:)'
        self.assertEqual(output, expected)

class TestLeafNode(unittest.TestCase):
    def setUp(self):
        self.paragraph_node = LeafNode(tag="p", value="Hello, world!")
        self.anchor_node = LeafNode(tag="a", value="Click me!", props={"href":"https://www.google.com"})
        self.text_node = LeafNode(tag=None, value="Raw text")
        self.wrong_leafnode = LeafNode(tag=None, value=None)

    def test_leaf_to_html_p(self):
        self.assertEqual(self.paragraph_node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_with_attr_to_html(self):
        self.assertEqual(self.anchor_node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_with_text_only(self):
        self.assertEqual(self.text_node.to_html(), "Raw text")
    
    def test_wrong_leaf(self):
        self.assertRaises(ValueError, self.wrong_leafnode.to_html)