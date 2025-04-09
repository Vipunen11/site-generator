import re

# Regex alt text and image url as tuples from markdown 
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

# Regex anchor text and url as tuples from markdown
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
