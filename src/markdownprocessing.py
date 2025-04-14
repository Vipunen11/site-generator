import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list" 

# Regex alt text and image url as tuples from markdown 
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

# Regex anchor text and url as tuples from markdown
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    fixed_blocks = []
    for split in split_blocks:
        stripped_split = split.strip()
        if stripped_split != "":
            fixed_blocks.append(stripped_split)
    return fixed_blocks

def block_to_blocktype(block):
    if block[0] == "#":
        return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    split_lines = block.split("\n")
    quotelines = 0
    listlines = 0
    ordered_lines = 0
    for split in split_lines:
        if split[0] == ">":
            quotelines += 1
        if split[:2] == "- ":
            listlines += 1
        if split[:3] == f"{ordered_lines+1}. ":
            ordered_lines += 1
    if len(split_lines) == quotelines:
        return BlockType.QUOTE
    if len(split_lines) == listlines:
        return BlockType.UNORDERED_LIST
    if len(split_lines) == ordered_lines:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def extract_title(markdown):
    split_lines = markdown.split("\n")
    for line in split_lines:
        stripped_line = line.strip()
        if stripped_line[:2] == "# ":
            return stripped_line[1:].strip()
    raise Exception("No Header found")
