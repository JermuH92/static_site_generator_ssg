import unittest
from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_inline_uneven_delimiter(self):
        node = TextNode("This is a test block for missing **bold delimiter.", TextType.PLAIN_TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

        self.assertEqual (
            str(context.exception),
            "Error: Delimiter is not matched or is not valid Markdown syntax."
        )

    def test_inline_multiple_delimiters(self):
        node = TextNode("a **b** c **d** e", TextType.PLAIN_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("a ", TextType.PLAIN_TEXT),
            TextNode("b", TextType.BOLD_TEXT),
            TextNode(" c ", TextType.PLAIN_TEXT),
            TextNode("d", TextType.BOLD_TEXT),
            TextNode(" e", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_inline_bold_eq(self):
        node = TextNode("some text **bold part** more text", TextType.PLAIN_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("some text ", TextType.PLAIN_TEXT),
            TextNode("bold part", TextType.BOLD_TEXT),
            TextNode(" more text", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_inline_italic_eq(self):
        node = TextNode("some text _italic part_ more text", TextType.PLAIN_TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        expected = [
            TextNode("some text ", TextType.PLAIN_TEXT),
            TextNode("italic part", TextType.ITALIC_TEXT),
            TextNode(" more text", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_inline_code_eq(self):
        node = TextNode("some text `code part` more text", TextType.PLAIN_TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [
            TextNode("some text ", TextType.PLAIN_TEXT),
            TextNode("code part", TextType.CODE_TEXT),
            TextNode(" more text", TextType.PLAIN_TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_inline_plain_text(self):
        node = TextNode("This text doesn't have any delimiters", TextType.PLAIN_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [TextNode("This text doesn't have any delimiters", TextType.PLAIN_TEXT)]
        self.assertListEqual(result, expected)
    
    def test_inline_non_plain_passthrough(self):
        node = TextNode("already bold", TextType.BOLD_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [TextNode("already bold", TextType.BOLD_TEXT)]
        self.assertListEqual(result, expected)
    
    
    
