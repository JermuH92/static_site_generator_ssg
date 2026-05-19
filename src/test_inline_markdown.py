import unittest
from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_uneven_delimiter(self):
        node = TextNode("This is a test block for missing **bold delimiter.", TextType.PLAIN_TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        self.assertEqual (
            str(context.exception),
            "Error: Delimiter is not matched or is not valid Markdown syntax."
        )