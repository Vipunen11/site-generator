from textnode import *
from htmlnode import *
from markdownprocessing import *

def main():
    print(text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))

main()
