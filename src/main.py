from textnode import *
from htmlnode import *
from markdownprocessing import *

def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

1. ordered
2. list
3. here

- unordered
- list
- here

> quote
> block
> here


This is another paragraph with _italic_ text and `code` here

"""
    html_node = markdown_to_html_node(md)
    print(html_node.to_html())
main()
