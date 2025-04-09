from textnode import *
from htmlnode import *
from markdownprocessing import *

def main():
    someTextNode = TextNode("This is some **bold markup** text", TextType.TEXT)
    someOtherNode = TextNode("This is some more text with **bold** word **hell** it has **multiple**", TextType.TEXT)
    other_new_nodes = split_nodes_delimiter([someTextNode, someOtherNode], "**", TextType.BOLD)
    print(other_new_nodes)

main()
