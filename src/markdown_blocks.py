from enum import Enum
from htmlnode import *
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes
from textnode import (
    text_node_to_html_node,
)

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    if block.startswith("> "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
            
        return BlockType.QUOTE
    
    if block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
            
        return BlockType.U_LIST
    
    if block.startswith("1. "):
        lines = block.split("\n")
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.O_LIST
    
    return BlockType.PARAGRAPH


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        
    raise ValueError("No h1-sized header found in markdown file")


def heading_to_html_node(block):
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break

    heading = block[heading_level:].strip()
    return ParentNode(f"h{heading_level}", text_to_children(heading))


def code_to_html_node(block):
    code = block[4:-3]
    raw_node = TextNode(code, TextType.PLAIN_TEXT)
    leaf_node = text_node_to_html_node(raw_node)
    code_parent = ParentNode("code", [leaf_node])
    pre_parent = ParentNode("pre", [code_parent])

    return pre_parent


def quotes_to_html_node(block):
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        new_line = line.strip("> ")
        new_lines.append(new_line)
    
    quotes = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(quotes))


def unordered_to_html_node(block):
    ul_lines = block.split("\n")
    li_nodes = []

    for line in ul_lines:
        text = line[2:]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    
    return ParentNode("ul", li_nodes)


def ordered_to_html_node(block):
    ol_lines = block.split("\n")
    li_nodes = []

    for i, line in enumerate(ol_lines):
        prefix_len = len(f"{i + 1}. ")
        text = line[prefix_len:]

        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    
    return ParentNode("ol", li_nodes)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)

    return ParentNode("p", children)
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            
            case BlockType.QUOTE:
                children.append(quotes_to_html_node(block))
            
            case BlockType.U_LIST:
                children.append(unordered_to_html_node(block))
            
            case BlockType.O_LIST:
                children.append(ordered_to_html_node(block))
            
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
                  
    return ParentNode("div", children)


