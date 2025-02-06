import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_created(self):
        node = HTMLNode("tag", "value", [HTMLNode("othertag", "othervalue")])
        return isinstance(node, HTMLNode)
    
    def test_to_str(self):
        node = str(HTMLNode("tag", "value", None, {"href": "https://www.google.com"}))
        self.assertEqual(node, """HTMLNode(tag, value, None, {'href': 'https://www.google.com'})""")

    def test_to_str_children(self):
        node = str(HTMLNode("tag", None, [HTMLNode("tag", "value")], None))
        self.assertEqual(node, """HTMLNode(tag, None, [HTMLNode(tag, value, None, None)], None)""")

    def test_props_to_html(self):
        node = HTMLNode("tag", "value", None, {"href": "https://www.google.com"})
        html = node.props_to_html()
        self.assertEqual(html, ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("tag", "value", None, {"href": "https://www.google.com", "target": "_blank"})
        html = node.props_to_html()
        self.assertEqual(html, ' href="https://www.google.com" target="_blank"')

    def test_leaf_node_to_html(self):
        node_1 = LeafNode("p", "This is a paragraph of text.")
        node_2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node_1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node_2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_parent_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_parent_node_to_html_nested(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        base_node = ParentNode("a", [node])
        self.assertEqual(base_node.to_html(), "<a><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></a>")

    def test_parent_node_to_html_no_children(self):
        node = ParentNode(
            "p",
            [],
        )
        with self.assertRaisesRegex(ValueError, "ParentNode does not have children"):
            node.to_html()

    def test_parent_node_to_html_no_tag(self):
        node = ParentNode(
            "",
            [LeafNode("i", "italic text")],
        )
        with self.assertRaisesRegex(ValueError, "ParentNode does not have tag"):
            node.to_html()
    
    def test_parent_node_to_html_nested_simple(self):
        x = LeafNode("b", "Bold text")
        a = ParentNode("span", [x])
        b = ParentNode("div", [a])
        self.assertEqual(b.to_html(), "<div><span><b>Bold text</b></span></div>")



if __name__ == "__main__":
    unittest.main()
    