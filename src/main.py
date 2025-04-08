from textnode import *
from htmlnode import *

def main():
    SomeTextNode = TextNode("This is some text", TextType.TEXT, "https://www.boot.dev")
    print(SomeTextNode)
    SomeLeafNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(SomeLeafNode.to_html())
    SomeParentNode = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),],)
    print(SomeParentNode.to_html())
    grandchild_node2 = LeafNode("p", "grandchild2")
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node, grandchild_node2])
    parent_node = ParentNode("div", [child_node])
    print(parent_node.to_html())

main()
