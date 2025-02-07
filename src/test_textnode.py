import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from textnode_parsers import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, None)
        node2 = TextNode("This is a text node", TextType.IMAGE, None)
        self.assertEqual(node, node2)

    def test_text_node_to_html_node(self):
        text_node = TextNode("Test text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(None, "Test text"))

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Test text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("b", "Test text"))

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Test text", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("a", "Test text", {"href": "https://google.com"}))

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



if __name__ == "__main__":
    unittest.main()