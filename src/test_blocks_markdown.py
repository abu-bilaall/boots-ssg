import unittest
from blocks_markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_with_doc(self):
        doc_md = """
# This is heading 1

## This is heading 2

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(doc_md)
        self.assertEqual(
            blocks,
            [
                "# This is heading 1",
                "## This is heading 2",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ]
        )

    def test_block_to_block_type_with_quote(self):
        quote = block_to_block_type("> this is a quote\n> still a quote\n> yep, quote")
        self.assertEqual(quote,BlockType.QUOTE)
    
    def test_block_to_block_type_with_heading(self):
        heading = block_to_block_type("### header 3")
        self.assertEqual(heading, BlockType.HEADING)
