from textnode import *
from htmlnode import *
from markdownprocessing import *

def main():
    someTextNode = TextNode("This is some **bold markup** text", TextType.TEXT)
    someOtherNode = TextNode("This is some more text with **bold** word **hell** it has **multiple**", TextType.TEXT)
    other_new_nodes = split_nodes_delimiter([someTextNode, someOtherNode], "**", TextType.BOLD)
    #print(other_new_nodes)
    testImageNode = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) funny picture of ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) here he is again ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)
    new_image_nodes = split_nodes_image([testImageNode])
    print(new_image_nodes)
    testLinkNode = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
    new_link_nodes = split_nodes_link([testLinkNode])
    print(new_link_nodes)
main()
