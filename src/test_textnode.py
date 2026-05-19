import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node4 = TextNode("This is a text node", TextType.CODE_TEXT)
        self.assertNotEqual(node3, node4)
    
    def test_for_none(self):
        node5 = TextNode("This is more text", TextType.ITALIC_TEXT)
        node6 = TextNode("This is more text", TextType.ITALIC_TEXT, "https://www.boot.dev")
        self.assertNotEqual(node5, node6)
    
    def test_repr(self):
        node = TextNode("This is even more text", TextType.CODE_TEXT, "https://example.com")
        self.assertEqual(repr(node), "TextNode(This is even more text, code, https://example.com)")
    
    def test_plain_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_tags(self):
        node = TextNode("This is bold text", TextType.BOLD_TEXT)
        node2 = TextNode("This is italic text", TextType.ITALIC_TEXT)
        node3 = TextNode("This is code text", TextType.CODE_TEXT)

        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        html_node3 = text_node_to_html_node(node3)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

        self.assertEqual(html_node2.tag, "i")
        self.assertEqual(html_node2.value, "This is italic text")

        self.assertEqual(html_node3.tag, "code")
        self.assertEqual(html_node3.value, "This is code text")
    
    def test_link_img_tags(self):
        node_link = TextNode("This is a link text", TextType.LINK_TEXT, "https://boot.dev")
        node_image = TextNode("This is an image", TextType.IMAGE_TEXT, "https://notareal.pic.pic.com/picture.png")

        html_node = text_node_to_html_node(node_link)
        html_node2 = text_node_to_html_node(node_image)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text")

        self.assertEqual(html_node2.tag, "img")
        self.assertEqual(html_node2.value, "")

        self.assertEqual(html_node.props, {"href": "https://boot.dev"})
        self.assertEqual(html_node2.props, {"src": "https://notareal.pic.pic.com/picture.png", "alt": "This is an image"})
    
    def test_no_enum_match(self):
        node = TextNode("Text", "TextType.NOT_REAL_ENUM")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    

if __name__ == "__main__":
    unittest.main()