import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_format(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_to_html_raises(self):
        node = HTMLNode("p", "hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_for_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')
    
    def test_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), '')
    
    def test_repr(self):
        node = HTMLNode("tag", "value", ['list_item'], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), "HTMLNode(tag, value, ['list_item'], {'href': 'https://www.google.com', 'target': '_blank'})")
