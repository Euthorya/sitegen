import unittest

from textnode import TextNode, TextType
from textnode_parsers import extract_markdown_images, extract_markdown_links, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_text_node_parser(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
    
    def test_text_node_parser_bold(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("bold", TextType.BOLD),
            ])

    def test_text_node_parser_italic(self):
        node = TextNode("test for *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("test for ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            ])
        
    def test_text_node_parser_italic_double(self):
        node = TextNode("test for *italic* and *another*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("test for ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.ITALIC),
            ])
    
    def test_text_node_parser_bold_and_italic(self):
        node = TextNode("test for *italic* and **bold**", TextType.TEXT)
        bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(bold_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("test for ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            ])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted = extract_markdown_images(text)
        self.assertEqual(extracted, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted = extract_markdown_links(text)
        self.assertEquals(extracted, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

if __name__ == "__main__":
    unittest.main()