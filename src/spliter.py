
from textnode import TextNode, TextType, text_node_to_html_node
import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception ("text not properly enclosed")
        ind_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                ind_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                ind_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(ind_nodes)
    return new_nodes

def extract_markdown_images(text):
    result: list[tuple] = []
    alt_text = re.findall(r"!\[([^\[\]]*)\]", text)
    urls = re.findall(r"\(([^\(\)]*)\)", text)
    for i in range(len(alt_text)):
        result.append((alt_text[i], urls[i]))
    return result

def extract_markdown_links(text):
    result: list[tuple] = []
    alt_text = re.findall(r"(?<!!)\[([^\[\]]*)\]", text)
    urls = re.findall(r"\(([^\(\)]*)\)", text)
    for i in range(len(alt_text)):
        result.append((alt_text[i], urls[i]))
    return result

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
              new_nodes.append(old_node)
              continue
        for link in links:
              sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
              if len(sections) != 2:
                  raise ValueError("invalid markdown, link section not closed")
              if sections[0] != "":
                  new_nodes.append(TextNode(sections[0], TextType.TEXT))
              new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
              original_text = sections[1]
        if original_text != "":
              new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text = text.strip("\n")
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "" or block == "\n":
            continue
        else:
            new_block = block.strip("\n")
            new_blocks.append(new_block.strip())
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
def block_to_block_type(block: str):
    if len(re.findall(r"^#{1,6}\s\w+", block)) != 0:
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    is_quote = True
    for line in block.split("\n"):
        if not line.startswith(">"):
            is_quote = False
    if is_quote:
        return BlockType.QUOTE
    is_unordered_list = True
    for line in block.split("\n"):
        if not line.startswith("- "):
            is_unordered_list = False
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    is_ordered_list = True
    lines = block.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        if not line.startswith(f"{i+1}. "):
            is_ordered_list = False
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def children_to_text(block:str, block_type)-> list:
    block = block.strip("\n")
    if block_type != BlockType.CODE:
        if block_type == BlockType.PARAGRAPH:
            segments = block.split("\n")
            block = " ".join(segments)
        if block_type == BlockType.QUOTE:
            block = block[1:]
            block = block.strip()
        if block_type == BlockType.HEADING:
            block = block.strip("#")
            block = block.strip()
        children = text_to_textnodes(block)
        html_children = []
        if block_type == BlockType.ORDERED_LIST or block_type ==  BlockType.UNORDERED_LIST:
            news = block.split("\n")
            for new in news:
                new = new[2:]
                new = new.strip()
                new_text_nodes = text_to_textnodes(new)
                for a in new_text_nodes:
                    child = ParentNode("li",[text_node_to_html_node(a)])
                    html_children.append(child)
            return html_children
        for child in children:
            html_children.append(text_node_to_html_node(child))
        return html_children
    else:
        new_block = block.strip("```")
        new_block = new_block[1:]
        return [LeafNode(None,new_block)]

def block_tag(block, block_type: BlockType)-> str:

    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            i = 0
            while block[i] == "#":
                i +=1
            return f"h{i}"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.CODE:
            return "code"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.UNORDERED_LIST:
            return "ul"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children = children_to_text(block, block_type)
        tag = block_tag(block, block_type)
        if block_type == BlockType.PARAGRAPH or block_type == BlockType.HEADING or block_type == BlockType.QUOTE:
            html_block = ParentNode(tag, children)
            html_blocks.append(html_block)
        elif block_type == BlockType.CODE:
            html_child = ParentNode(tag, children)
            html_block = ParentNode("pre", [html_child])
            html_blocks.append(html_block)
        else:
            html_block = ParentNode(tag, children)
            html_blocks.append(html_block)
    result_node = ParentNode("div", html_blocks)
    return result_node
