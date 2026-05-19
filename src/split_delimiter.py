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