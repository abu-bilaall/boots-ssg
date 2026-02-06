import unittest
from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_awesome_title(self):
        md = """
Some intro text

# My Awesome Title
More content here
"""
        title = extract_title(md)
        self.assertEqual(title, "My Awesome Title")

    def test_title_at_top_of_file(self):
        md = "# Hello World\nSome content"
        title = extract_title(md)
        self.assertEqual(title, "Hello World")

    def test_title_with_leading_whitespace(self):
        md = """
            # Indented Title
        """
        title = extract_title(md)
        self.assertEqual(title, "Indented Title")

    def test_title_with_extra_spaces(self):
        md = "#    Spaced Out Title   "
        title = extract_title(md)
        self.assertEqual(title, "Spaced Out Title")

    def test_title_with_special_characters(self):
        md = "# Hello, World! 🚀🔥"
        title = extract_title(md)
        self.assertEqual(title, "Hello, World! 🚀🔥")

    def test_multiple_headings_uses_first_top_level(self):
        md = """
# First Title
Some text
# Second Title
"""
        title = extract_title(md)
        self.assertEqual(title, "First Title")

    def test_ignores_subheadings(self):
        md = """
## Not the Title
Some text
"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_missing_title_raises_error(self):
        md = """
Some intro text
No headings here
"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_empty_string_raises_error(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_whitespace_only_raises_error(self):
        with self.assertRaises(ValueError):
            extract_title("   \n   \n")
