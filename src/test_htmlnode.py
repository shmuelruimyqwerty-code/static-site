
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from page_gen import extract_title

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("tag string", "value string",None,{
            "href": "https://www.google.com",
            "target": "_blank",
        })
        node2 = HTMLNode("tag str", "val string",None,{
            "href": "https://www.boot.dev.com",
            "target": "_blank",
        })
        node3 = HTMLNode("TagString", "value_string",None,{
            "href": "https://www.google.com",
            "target": "_blank",
        })

    def test_leaf_to_html_p(self):
            node = LeafNode("p", "Hello, world!")
            self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
            node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            self.assertEqual(node2.to_html(),'<a href="https://www.google.com">Click me!</a>')
            node3 = LeafNode("h", "hello world", {"href": "https://www.amazon.com"})
            self.assertEqual(node3.to_html(),'<h href="https://www.amazon.com">hello world</h>')


    def test_to_html_with_children(self):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
            grandchild_node = LeafNode("b", "grandchild")
            random_node = LeafNode("a", "random")
            child_node = ParentNode("span", [grandchild_node,random_node])
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b><a>random</a></span></div>",
            )
    def test_header(self):
        md = "#     header        "
        result = extract_title(md)
        self.assertEqual(result,"header",)
if __name__ == "__main__":
    unittest.main()
