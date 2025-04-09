from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, TextType, url=None):
        self.text = text
        self.text_type = TextType
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

#Function to convert text nodes to html nodes
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case(text_node.text_type.TEXT):
            return LeafNode(None, text_node.text)
        case(text_node.text_type.BOLD):
            return LeafNode("b", text_node.text)
        case(text_node.text_type.ITALIC):
            return LeafNode("i", text_node.text)
        case(text_node.text_type.CODE):
            return LeafNode("code", text_node.text)
        case(text_node.text_type.LINK):
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case(text_node.text_type.IMAGE):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Text type is not one of valid formats")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_old_node = old_node.text.split(delimiter)
            #Catch invalid markup, where there is no closing delimiter, ergo splits are divisible by 2
            if len(split_old_node) % 2 == 0:
                raise Exception("Invalid markup, no closing delimiter found")
            #Iterate over splits, flip-flopping delimiter_found boolean to mark when a split is before a delimiter or after one
            delimiter_found = False
            for split in split_old_node:
                if delimiter_found == False:
                    new_nodes.append(TextNode(split, TextType.TEXT))
                    delimiter_found = True
                elif delimiter_found == True:
                    new_nodes.append(TextNode(split, text_type))
                    delimiter_found = False


    return new_nodes
