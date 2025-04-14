import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="h1", value="This is some text", props={"bogos": "binted"})
        node2 = HTMLNode(tag="h1", value="This is some text", props={"bogos": "binted"})
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = HTMLNode(tag="h1", value="This is some text", props={"bogos": "binted"})
        node2 = HTMLNode(tag="h1", value="This is some text", props={"photos": "printed"})
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = HTMLNode(tag="h1", value="This is some text", props={"bogos": "binted"})
        node2 = HTMLNode(tag="h1", value="This is some text", children="many", props={"bogos": "binted"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode(tag="h1", value="This is some text", props={"bogos": "binted"})
        self.assertEqual(
            "HTMLNode, tag: h1, value: This is some text, children: None, props: {'bogos': 'binted'}", repr(node)
        )

    def test_proprs_to_html(self):
        node = HTMLNode(tag="h1", value="This is some text", props={"bogos": "binted"})
        self.assertEqual(' bogos="binted"', node.props_to_html())

    def test_to_html(self):
        node = HTMLNode(tag="h1", value="This is some text", props={"bogos": "binted"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), f'<a href="https://www.google.com">Click me!</a>')


    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)

if __name__ == "__main__":
    unittest.main()
