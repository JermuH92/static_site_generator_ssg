import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.TEXT_PLAIN)
        node4 = TextNode("This is a text node", TextType.CODE_TEXT)
        self.assertNotEqual(node3, node4)
    
    def test_for_none(self):
        node5 = TextNode("This is more text", TextType.ITALIC_TEXT)
        node6 = TextNode("This is more text", TextType.ITALIC_TEXT, "https://www.boot.dev")
        self.assertNotEqual(node5, node6)
    
    def test_repr(self):
        node = TextNode("This is even more text", TextType.CODE_TEXT, "https://example.com")
        self.assertEqual(repr(node), "TextNode(This is even more text, code, https://example.com)")

    

if __name__ == "__main__":
    unittest.main()