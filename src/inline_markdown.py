import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        split_text = current_text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise Exception("Error: Delimiter is not matched or is not valid Markdown syntax.")

        for index, value in enumerate(split_text):
            if value == "":
                continue

            if index % 2 == 0:
                new_nodes.append(TextNode(value, TextType.PLAIN_TEXT))

            else:
                new_nodes.append(TextNode(value, text_type))
            
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text == "":
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image_alt, image_link in images:

            image_link_markdown = f"![{image_alt}]({image_link})"
            sections = original_text.split(image_link_markdown, 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed.")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE_TEXT, image_link))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
    
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text == "":
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link_text, link in links:

            link_markdown = f"[{link_text}]({link})"
            sections = original_text.split(link_markdown, 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed.")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK_TEXT, link))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    
    return nodes


def extract_markdown_images(text):
    regex_matches_image = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return regex_matches_image


def extract_markdown_links(text):
    regex_matches_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return regex_matches_link