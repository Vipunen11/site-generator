from htmlnode import *
from enum import Enum
from markdownprocessing import *
import re

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
                    if split != "":
                        new_nodes.append(TextNode(split, TextType.TEXT))
                    delimiter_found = True
                elif delimiter_found == True:
                    new_nodes.append(TextNode(split, text_type))
                    delimiter_found = False


    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_old_node = re.split(r"!\[(.*?)\]\((.*?)\)", old_node.text)
            matching_tuples = extract_markdown_images(old_node.text)
            #initialize boolean, used later for matching alt text with links
            alt_text_found = False
            #Matches list is a list of markdown tags that we compare our splits against later. A loop is used to unpack the tuples form the matching_tuples list into a "flat" list
            matches = []
            for matching_tuple in matching_tuples:
                for item in matching_tuple:
                    matches.append(item)
            #Iterate over splits, alt text found is used for matching alt text with its corresponding link.
            for split in split_old_node:
                if split in matches:
                    if alt_text_found == True:
                        new_nodes.append(TextNode(alt_text, TextType.IMAGE, split))
                        alt_text_found = False
                    else:
                        alt_text = split
                        alt_text_found = True
                elif split != "":
                    new_nodes.append(TextNode(split, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_old_node = re.split(r"\[(.*?)\]\((.*?)\)", old_node.text)
            matching_tuples = extract_markdown_links(old_node.text)
            #initialize boolean, used later for matching alt text with links
            alt_text_found = False
            #Matches list is a list of markdown tags that we compare our splits against later. A loop is used to unpack the tuples form the matching_tuples list into a "flat" list
            matches = []
            for matching_tuple in matching_tuples:
                for item in matching_tuple:
                    matches.append(item)
            #Iterate over splits, alt text found is used for matching alt text with its corresponding link.
            for split in split_old_node:
                if split in matches:
                    if alt_text_found == True:
                        new_nodes.append(TextNode(alt_text, TextType.LINK, split))
                        alt_text_found = False
                    else:
                        alt_text = split
                        alt_text_found = True
                elif split != "":
                    new_nodes.append(TextNode(split, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    bolded = split_nodes_delimiter([initial_node], "**", TextType.BOLD)
    italics = split_nodes_delimiter(bolded, "_", TextType.ITALIC)
    coded = split_nodes_delimiter(italics, "`", TextType.CODE)
    images = split_nodes_image(coded)
    linked = split_nodes_link(images)
    return linked

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = list(map(text_node_to_html_node, textnodes))
    return children


def markdown_to_html_node(markdown):
    split_markdown = markdown_to_blocks(markdown)
    html_nodes = []
    for split_block in split_markdown:
        html_node = block_to_html_node(split_block)
        html_nodes.append(html_node)
    return ParentNode("div", html_nodes)

def block_to_html_node(block):
    block_type = block_to_blocktype(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("Invalid Block Type!")



def paragraph_to_html_node(block):
    split_block = block.split("\n")
    joined_paragraph = " ".join(split_block)
    return ParentNode("p", text_to_children(joined_paragraph))

def heading_to_html_node(block):
    heading_number = 0
    for char in block:
        if char == "#":
            heading_number += 1
        else:
            break
    text = block[heading_number+1:]
    return ParentNode(f"h{heading_number}", text_to_children(text))

def code_to_html_node(block):
    node = TextNode(block[4:-3], TextType.CODE)
    child_node = text_node_to_html_node(node)
    return ParentNode("pre", [child_node,])
    
def ordered_list_to_html_node(block):
    split_block = block.split("\n")
    fixed_splits = []
    for split in split_block:
        text = split[3:]
        children = text_to_children(text)
        fixed_splits.append(ParentNode("li", children))
    return ParentNode("ol", fixed_splits)

def unordered_list_to_html_node(block):
    split_block = block.split("\n")
    fixed_splits = []
    for split in split_block:
        text = split[2:]
        children = text_to_children(text)
        fixed_splits.append(ParentNode("li", children))
    return ParentNode("ul", fixed_splits)

def quote_to_html_node(block):
    split_block = block.split("\n")
    fixed_splits = []
    for split in split_block:
        fixed_splits.append(split.lstrip(">").strip())
    children = text_to_children(" ".join(fixed_splits))
    return ParentNode("blockquote", children)
