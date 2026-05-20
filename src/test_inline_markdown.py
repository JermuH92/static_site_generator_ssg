import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
)
from textnode import TextNode, TextType

########### SPLIT_NODES_DELIMITER CLASS STARTS HERE ###########

class TestSplitNodesDelimiter(unittest.TestCase):

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

########### SPLIT_NODES_DELIMITER CLASS ENDS HERE ###########

########### SPLIT_NODES_IMAGE CLASS STARTS HERE ###########

class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode(
                "second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

########### REGEX EXTRACTION CLASS STARTS HERE ###########

class TestRegexExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![cat](https://cats.com/cat.png) and ![dog](https://dogs.com/dog.png)"
        )
        self.assertListEqual(
            [("cat", "https://cats.com/cat.png"), ("dog", "https://dogs.com/dog.png")],
            matches,
        )
    
    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This has no images at all")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[cat](https://cats.com) and [dog](https://dogs.com)"
        )
        self.assertListEqual(
            [("cat", "https://cats.com"), ("dog", "https://dogs.com")],
            matches,
        )
    
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This has no links at all")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_not_images(self):
        matches = extract_markdown_links(
            "![image](https://img.com/a.png) and [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)
    
########### REGEX EXTRACTION CLASS ENDS HERE ###########    
