from enum import Enum
from platform import node
import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from textnode import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_type(self):
        node = TextNode("hello", TextType.TEXT)
        node2 = TextNode("hello", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_text(self):
        node = TextNode("hello", TextType.TEXT)
        node2 = TextNode("world", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_url(self):
        node = TextNode("hello", TextType.LINK, url="https://example.com")
        node2 = TextNode("hello", TextType.LINK, url="https://example.org")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")

    def test_italic(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")

    def test_code(self):
        node = TextNode("This is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, (""))
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "This is an image"})

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT)
        expected_repr = "TextNode(This is a text node, text, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_unsupported_text_type(self):
        class UnsupportedTextType(Enum):
            UNSUPPORTED = "unsupported"
        node = TextNode("This is unsupported", UnsupportedTextType.UNSUPPORTED)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a text node")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_with_formatting(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_with_unmatched_delimiter(self):
        node = TextNode("This is *italic text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_split_nodes_delimiter_with_multiple_formatting(self):
        node = TextNode("This is *italic* and **bold** text", TextType.TEXT)
        after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        final = split_nodes_delimiter(after_bold, "*", TextType.ITALIC)
        self.assertEqual(len(final), 5)
        self.assertEqual(final[0].text, "This is ")
        self.assertEqual(final[0].text_type, TextType.TEXT)
        self.assertEqual(final[1].text, "italic")
        self.assertEqual(final[1].text_type, TextType.ITALIC)
        self.assertEqual(final[2].text, " and ")
        self.assertEqual(final[2].text_type, TextType.TEXT)
        self.assertEqual(final[3].text, "bold")
        self.assertEqual(final[3].text_type, TextType.BOLD)
        self.assertEqual(final[4].text, " text")
        self.assertEqual(final[4].text_type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()
                         