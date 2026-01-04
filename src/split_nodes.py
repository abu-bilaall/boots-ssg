from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimited_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            delimited_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(
                    f"Unmatched delimiter '{delimiter}' in text: {node.text}"
                )
            
            delimited_nodes.extend(
                (
                    TextNode(part, TextType.PLAIN)
                    if index % 2 == 0
                    else TextNode(part, text_type)
                )
                for index, part in enumerate(parts)
            )
            
    return delimited_nodes
