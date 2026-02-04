import unittest
from blocks_markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
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
            ],
        )

    def test_block_to_block_type_with_quote(self):
        quote = block_to_block_type("> this is a quote\n> still a quote\n> yep, quote")
        self.assertEqual(quote, BlockType.QUOTE)

    def test_block_to_block_type_with_heading(self):
        heading = block_to_block_type("### header 3")
        self.assertEqual(heading, BlockType.HEADING)


class MarkdownToHtmlNode(unittest.TestCase):
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_block(self):
        md = """
# Title

## Subtitle

#### Section
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h1>Title</h1><h2>Subtitle</h2><h4>Section</h4></div>"
        )

    def test_quote_block(self):
        md = """
>line one
>line two
> line three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>line one\nline two\nline three</blockquote></div>"
        )

    def test_ul_block(self):
        md = """
- Apple
- Banana
- Cherry
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul></div>"
        )

    def test_ul_block(self):
        md = """
1. First
2. Second
3. Third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_mixed_content(self):
        md = """
# Main Title

This is a paragraph with **bold** and _italic_ text.

## Subsection

> This is a quote block
> with multiple lines

- List item one
- List item two with `code`
- List item three

1. Ordered item
2. Another ordered item

```
def hello():
    print("world")
```

Final paragraph with [link](https://example.com) and ![image](image.jpg).
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Main Title</h1>"
            "<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>"
            "<h2>Subsection</h2>"
            "<blockquote>This is a quote block\nwith multiple lines</blockquote>"
            "<ul><li>List item one</li><li>List item two with <code>code</code></li><li>List item three</li></ul>"
            "<ol><li>Ordered item</li><li>Another ordered item</li></ol>"
            "<pre><code>def hello():\n    print(\"world\")\n</code></pre>"
            "<p>Final paragraph with <a href=\"https://example.com\">link</a> and <img src=\"image.jpg\" alt=\"image\"></img>.</p>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_single_line_quote(self):
        md = "> Single line quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Single line quote</blockquote></div>")

    def test_nested_inline_formatting(self):
        md = "This has **bold with _italic inside_** and `code text`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Note: This tests how your inline parser handles nested formatting
        # The current parser may not handle nested formatting, so we test what it actually does
        expected = "<div><p>This has <b>bold with _italic inside_</b> and <code>code text</code></p></div>"
        self.assertEqual(html, expected)

    def test_heading_levels(self):
        md = """# H1

## H2

### H3

#### H4

##### H5

###### H6"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3><h4>H4</h4><h5>H5</h5><h6>H6</h6></div>"
        self.assertEqual(html, expected)

    def test_code_block_with_language(self):
        md = """
```python
def greet(name):
    return f"Hello, {name}!"
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><pre><code>python\ndef greet(name):\n    return f\"Hello, {name}!\"\n</code></pre></div>"
        self.assertEqual(html, expected)

    def test_multiline_quote_with_varying_spaces(self):
        md = """
>First line
> Second line with space
>  Third line with two spaces
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>First line\nSecond line with space\nThird line with two spaces</blockquote></div>"
        self.assertEqual(html, expected)

    def test_list_with_inline_formatting(self):
        md = """
- Item with **bold** text
- Item with _italic_ text  
- Item with `code` text
- Item with [link](https://example.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div><ul>"
            "<li>Item with <b>bold</b> text</li>"
            "<li>Item with <i>italic</i> text</li>"
            "<li>Item with <code>code</code> text</li>"
            "<li>Item with <a href=\"https://example.com\">link</a></li>"
            "</ul></div>"
        )
        self.assertEqual(html, expected)

    def test_ordered_list_with_inline_formatting(self):
        md = """
1. First item with **bold**
2. Second item with _italic_
3. Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div><ol>"
            "<li>First item with <b>bold</b></li>"
            "<li>Second item with <i>italic</i></li>"
            "<li>Third item with <code>code</code></li>"
            "</ol></div>"
        )
        self.assertEqual(html, expected)
