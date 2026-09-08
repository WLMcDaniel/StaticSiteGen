import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        expected_html = ' class="container" id="main"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_without_props(self):
        node = HTMLNode(tag="div")
        expected_html = ''
        self.assertEqual(node.props_to_html(), expected_html)

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"style": "color: red;"})
        expected_repr = "HTMLNode(p, Hello, [], {'style': 'color: red;'})"
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello")
        expected_html = "<p>Hello</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_tag(self):
        node = LeafNode(tag=None, value="Hello")
        expected_html = "Hello"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_props(self):
        node = LeafNode(tag="p", value="Hello", props={"style": "color: red;"})
        expected_html = '<p style="color: red;">Hello</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_repr(self):
        node = LeafNode(tag="p", value="Hello", props={"style": "color: red;"})
        expected_repr = "LeafNode(p, Hello, {'style': 'color: red;'})"
        self.assertEqual(repr(node), expected_repr)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_tag_and_children(self):
        child1 = LeafNode(tag="p", value="Hello")
        child2 = LeafNode(tag="p", value="World")
        node = ParentNode(tag="div", children=[child1, child2])
        expected_html = "<div><p>Hello</p><p>World</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_tag(self):
        child1 = LeafNode(tag="p", value="Hello")
        node = ParentNode(tag=None, children=[child1])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_without_children(self):
        node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        child1 = LeafNode(tag="p", value="Hello")
        node = ParentNode(tag="div", children=[child1], props={"class": "container"})
        expected_html = '<div class="container"><p>Hello</p></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_repr(self):
        child1 = LeafNode(tag="p", value="Hello")
        node = ParentNode(tag="div", children=[child1], props={"class": "container"})
        expected_repr = "ParentNode(div, [LeafNode(p, Hello, None)], {'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
