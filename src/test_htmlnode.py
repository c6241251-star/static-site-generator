import unittest
from htmlnode import HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("b", "Hiya boots", None, { "href": "https://www.google.com", "target": "_blank", })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", { "href": "https://www.google.com", "target": "_blank", })
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">Hello, world!</p>')


if __name__ == "__main__":
    unittest.main()