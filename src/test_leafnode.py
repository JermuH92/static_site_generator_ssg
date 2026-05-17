import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_raw_text(self):
        node = LeafNode(None, "Test for raw text when tag is none.")
        self.assertEqual(node.to_html(), "Test for raw text when tag is none.")
    
    def test_props_rendering(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')

    def test_for_value_error(self):
        node = LeafNode("img", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_repr(self):
        node = LeafNode("tag", "value", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), "LeafNode(tag, value, {'href': 'https://www.google.com', 'target': '_blank'})")

        