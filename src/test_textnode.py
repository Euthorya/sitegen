import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


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



if __name__ == "__main__":
    unittest.main()