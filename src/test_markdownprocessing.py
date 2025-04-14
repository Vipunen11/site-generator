import unittest

from markdownprocessing import *

class TestMarkDownProcessing(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted = extract_markdown_images(text)
        self.assertEqual(extracted, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted = extract_markdown_links(text)
        self.assertEqual(extracted, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )


    def test_block_to_blocktype_quote(self):
        block = ">this\n>is\n>a\n>Quote"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_block_to_blocktype_unordered(self):
        block = "- this\n- is\n- a\n- unordered list"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        block = "1. this\n2. is\n3. a\n4. ordered list"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)

    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")


if __name__ == "__main__":
    unittest.main()
