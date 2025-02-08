import unittest

from textnode import TextNode, TextType
from textnode_parsers import extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


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
        self.assertEqual(extracted, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        nodes =  [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertEqual(new_nodes, nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, nodes)


    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, nodes)

    def test_markdown_to_blocks(self):
        lines = markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item""")
        self.assertEqual(lines, ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
"""* This is the first list item in a list block
* This is a list item
* This is another list item"""])
        
    def test_markdown_to_blocks_newlines(self):
        lines = markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


    
* This is the first list item in a list block
* This is a list item
* This is another list item""")
        self.assertEqual(lines, ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
"""* This is the first list item in a list block
* This is a list item
* This is another list item"""])


if __name__ == "__main__":
    unittest.main()