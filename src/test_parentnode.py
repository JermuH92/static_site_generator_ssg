import unittest

from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_parent_breadth(self):
        node = LeafNode("b", "Bold text")
        node2 = LeafNode(None, "Normal text")
        node3 = LeafNode("i", "Italic text")

        parent_node = ParentNode("p", [node, node2, node3])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i></p>"
        )
    
    def test_parent_empty_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")
    
    def test_parent_tag_value_error(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_inheritance_through_recursion(self):        
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><a href="https://www.google.com" target="_blank">Click me!</a></div>'
        )