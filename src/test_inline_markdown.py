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
    
    def test_split_images_single(self):
        node = TextNode("![image one](https://localhost.first.png)", TextType.PLAIN_TEXT,)
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode("image one", TextType.IMAGE_TEXT, "https://localhost.first.png")], new_node)
        
    def test_split_images_multiple(self):
        node = TextNode(
            "First text ![image one](https://localhost.first.png) second text ![image two](https://localhost.second.png) third text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("First text ", TextType.PLAIN_TEXT),
            TextNode("image one", TextType.IMAGE_TEXT, "https://localhost.first.png"),
            TextNode(" second text ", TextType.PLAIN_TEXT),
            TextNode("image two", TextType.IMAGE_TEXT, "https://localhost.second.png"),
            TextNode(" third text", TextType.PLAIN_TEXT),
        ],
        new_nodes,
    )
    
    def test_split_images_mid_string(self):
        node = TextNode("Test picture ![cat](https://test.cat.pictures.cat/cat.png) in the middle", TextType.PLAIN_TEXT, )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("Test picture ", TextType.PLAIN_TEXT),
            TextNode("cat", TextType.IMAGE_TEXT, "https://test.cat.pictures.cat/cat.png"),
            TextNode(" in the middle", TextType.PLAIN_TEXT)
        ],
        new_nodes
    )
    
    def test_split_images_no_empty_nodes(self):
        node = TextNode(
            "![cat](https://test.cat.pictures.cat/cat.png) text only in middle ![dog](https://test.dog.pictures.dog/dog.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("cat", TextType.IMAGE_TEXT, "https://test.cat.pictures.cat/cat.png"),
            TextNode(" text only in middle ", TextType.PLAIN_TEXT),
            TextNode("dog", TextType.IMAGE_TEXT, "https://test.dog.pictures.dog/dog.png"),
        ],
        new_nodes
    )
    
    def test_split_images_consecutive(self):
        node = TextNode("![cat](https://test.cat.pictures.cat/cat.png)![dog](https://test.dog.pictures.dog/dog.png)", TextType.PLAIN_TEXT, )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("cat", TextType.IMAGE_TEXT, "https://test.cat.pictures.cat/cat.png"),
            TextNode("dog", TextType.IMAGE_TEXT, "https://test.dog.pictures.dog/dog.png"),
        ],
        new_nodes
    )
    
    def test_split_images_non_plain_passthrough(self):
        node = TextNode("This nodes text is **bold**", TextType.BOLD_TEXT)
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode("This nodes text is **bold**", TextType.BOLD_TEXT)], new_node)
        
    def test_split_images_no_images_return_original(self):
        node = TextNode("This node is just plain text", TextType.PLAIN_TEXT)
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode("This node is just plain text", TextType.PLAIN_TEXT)], new_node)

########### SPLIT_NODES_IMAGE CLASS ENDS HERE ###########

########### SPLIT_NODES_LINK CLASS STARTS HERE ###########

class TestSplitNodesLink(unittest.TestCase):

    def test_split_links_no_alt_text(self):
        node = TextNode("[](https://www.google.com)", TextType.PLAIN_TEXT,)
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.LINK_TEXT, "https://www.google.com")], new_node)

    def test_split_links_single(self):
        node = TextNode("[link to google](https://www.google.com)", TextType.PLAIN_TEXT,)
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode("link to google", TextType.LINK_TEXT, "https://www.google.com")], new_node)
    
    def test_split_links_multiple(self):
        node = TextNode(
            "First link text [enter site](https://www.youtube.com) second link text [enter site two](https://www.google.com) third link text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("First link text ", TextType.PLAIN_TEXT),
            TextNode("enter site", TextType.LINK_TEXT, "https://www.youtube.com"),
            TextNode(" second link text ", TextType.PLAIN_TEXT),
            TextNode("enter site two", TextType.LINK_TEXT, "https://www.google.com"),
            TextNode(" third link text", TextType.PLAIN_TEXT),
        ],
        new_nodes,
    )
    
    def test_split_links_mid_string(self):
        node = TextNode("Test link [to dashboard](https://boot.dev/dashboard) in the middle", TextType.PLAIN_TEXT, )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("Test link ", TextType.PLAIN_TEXT),
            TextNode("to dashboard", TextType.LINK_TEXT, "https://boot.dev/dashboard"),
            TextNode(" in the middle", TextType.PLAIN_TEXT)
        ],
        new_nodes
    )
    
    def test_split_links_no_empty_nodes(self):
        node = TextNode(
            "[link one](https://notanactualwebsite.web) text only in middle [link two](https://notarealsite.forreal.net)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("link one", TextType.LINK_TEXT, "https://notanactualwebsite.web"),
            TextNode(" text only in middle ", TextType.PLAIN_TEXT),
            TextNode("link two", TextType.LINK_TEXT, "https://notarealsite.forreal.net"),
        ],
        new_nodes
    )
    
    def test_split_links_consecutive(self):
        node = TextNode("[link](https://google.com)[link2](https://boot.dev)", TextType.PLAIN_TEXT, )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("link", TextType.LINK_TEXT, "https://google.com"),
            TextNode("link2", TextType.LINK_TEXT, "https://boot.dev"),
        ],
        new_nodes
    )
    
    def test_split_links_non_plain_passthrough(self):
        node = TextNode("This nodes text is **bold**", TextType.BOLD_TEXT)
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode("This nodes text is **bold**", TextType.BOLD_TEXT)], new_node)
        
    def test_split_links_no_links_return_original(self):
        node = TextNode("This node is just plain text", TextType.PLAIN_TEXT)
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode("This node is just plain text", TextType.PLAIN_TEXT)], new_node)
    
    def test_split_links_ignores_images(self):
        node = TextNode(
            "This node contains both link [link](https://google.com) and image ![cat](https://test.cat.pictures.cat/cat.png)", TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This node contains both link ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://google.com"),
            TextNode(" and image ![cat](https://test.cat.pictures.cat/cat.png)", TextType.PLAIN_TEXT),
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
