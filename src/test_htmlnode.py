import unittest

from htmlnode import HTMLNode


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
        self.assertEqual(html, 'href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("tag", "value", None, {"href": "https://www.google.com", "target": "_blank"})
        html = node.props_to_html()
        self.assertEqual(html, 'href="https://www.google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()
    