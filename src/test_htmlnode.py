import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")
    
    def test_to_html_with_multiple_children(self):
        title = LeafNode(tag="title", value="Document")
        style = LeafNode(tag="style", value="p {color: red;}")
        script = LeafNode(tag="script", value="test", props={"src": "myscript.js", "attributionsrc": "https://a.example/register-source https://b.example/register-source"})
        head = ParentNode(tag="head", children=[title, script, style])
        self.assertEqual(head.to_html(), '<head><title>Document</title><script src="myscript.js" attributionsrc="https://a.example/register-source https://b.example/register-source">test</script><style>p {color: red;}</style></head>')

    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag=None, children=[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children_raises_error(self):
        parent_node = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_single_child(self):
        child_node = LeafNode(tag="p", value="Hello world")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><p>Hello world</p></div>")

    def test_to_html_nested_parent_nodes(self):
        # Create deeply nested structure: div > section > article > p
        text_node = LeafNode(tag="p", value="Nested content")
        article_node = ParentNode(tag="article", children=[text_node])
        section_node = ParentNode(tag="section", children=[article_node])
        div_node = ParentNode(tag="div", children=[section_node])
        self.assertEqual(div_node.to_html(), "<div><section><article><p>Nested content</p></article></section></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node], props={"class": "container", "id": "main"})
        self.assertEqual(parent_node.to_html(), '<div class="container" id="main"><span>child</span></div>')