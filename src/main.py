from textnode import *
from htmlnode import *

def main():
    SomeTextNode = TextNode("This is some text", TextType.TEXT, "https://www.boot.dev")
    print(SomeTextNode)
    SomeLeafNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(SomeLeafNode.to_html())
    
    


main()
