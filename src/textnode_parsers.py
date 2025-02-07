from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        words = node.text.split(delimiter)
        if len(words) == 0:
            new_nodes.append(node)
        elif len(words) % 2 == 0:
            raise ValueError(f"Invalid markdown format for: {node}")
        else:
            for i, word in enumerate(words):
                if word:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(word, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(word, text_type))
    return new_nodes

def get_type(delimiter:str):
    match delimiter:
        case "`":
            return TextType.CODE
        case "*":
            return TextType.ITALIC
        case "**":
            return TextType.BOLD
