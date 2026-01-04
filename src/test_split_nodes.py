import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_split_single_delimiter_pair(self):
        """Test splitting a node with a single pair of delimiters"""
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_multiple_delimiter_pairs(self):
        """Test splitting a node with multiple pairs of delimiters"""
        node = TextNode("Text with `code1` and `code2` blocks", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_no_delimiters(self):
        """Test splitting a node with no delimiters"""
        node = TextNode("This is plain text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [TextNode("This is plain text", TextType.PLAIN)]
        
        self.assertEqual(result, expected)
    
    def test_split_delimiter_at_start(self):
        """Test splitting when delimiter is at the start"""
        node = TextNode("`code` at start", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_delimiter_at_end(self):
        """Test splitting when delimiter is at the end"""
        node = TextNode("Text ends with `code`", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text ends with ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_only_delimited_content(self):
        """Test splitting when the entire content is delimited"""
        node = TextNode("`entire content`", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("", TextType.PLAIN),
            TextNode("entire content", TextType.CODE),
            TextNode("", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_empty_delimited_content(self):
        """Test splitting with empty content between delimiters"""
        node = TextNode("Text with `` empty code", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("", TextType.CODE),
            TextNode(" empty code", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_non_plain_nodes_unchanged(self):
        """Test that non-plain nodes are not split"""
        nodes = [
            TextNode("This is `code`", TextType.BOLD),
            TextNode("This is `code`", TextType.ITALIC),
            TextNode("This is `code`", TextType.CODE)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # Non-plain nodes should remain unchanged
        self.assertEqual(result, nodes)
    
    def test_split_mixed_node_types(self):
        """Test splitting a mix of plain and non-plain nodes"""
        nodes = [
            TextNode("Plain with `code`", TextType.PLAIN),
            TextNode("Bold with `code`", TextType.BOLD),
            TextNode("Another plain with `more code`", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("Plain with ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.PLAIN),
            TextNode("Bold with `code`", TextType.BOLD),  # unchanged
            TextNode("Another plain with ", TextType.PLAIN),
            TextNode("more code", TextType.CODE),
            TextNode("", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_different_delimiters(self):
        """Test splitting with different delimiter types"""
        # Test with asterisk for bold
        node = TextNode("Text with *bold* word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_split_empty_input(self):
        """Test splitting with empty input list"""
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])
    
    def test_split_empty_text_node(self):
        """Test splitting a node with empty text"""
        node = TextNode("", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [TextNode("", TextType.PLAIN)]
        self.assertEqual(result, expected)
    
    def test_split_unmatched_delimiter_raises_exception(self):
        """Test that unmatched delimiters raise an exception"""
        node = TextNode("Text with `unmatched delimiter", TextType.PLAIN)
        
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

class TestCorrectedImplementation(unittest.TestCase):
    """Tests for the corrected implementation"""
    
    def test_corrected_basic_split(self):
        """Test the corrected implementation with basic case"""
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN)
        ]
        
        self.assertEqual(result, expected)
    
    def test_corrected_unmatched_delimiter(self):
        """Test that unmatched delimiters raise an error"""
        node = TextNode("Text with `unmatched delimiter", TextType.PLAIN)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()
