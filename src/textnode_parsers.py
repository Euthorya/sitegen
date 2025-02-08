import re
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

def extract_markdown_images(text:str):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text:str):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        line = node.text
        for i in images:
            text, rest = line.split(f"![{i[0]}]({i[1]})", 1)
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
            line = rest
        if line:
            new_nodes.append(TextNode(line, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_links(node.text)
        if not images:
            new_nodes.append(node)
            continue

        line = node.text
        for i in images:
            text, rest = line.split(f"[{i[0]}]({i[1]})", 1)
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(i[0], TextType.LINK, i[1]))
            line = rest
        if line:
            new_nodes.append(TextNode(line, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(i, TextType.TEXT) for i in text.split("\n")]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    block = []
    result = []
    for line in lines:
        line = line.strip()
        if line and line != "\n":
            block.append(line.strip())
        else:
            if block:
                result.append("\n".join(i for i in block))
                block = []
    if block:
        result.append("\n".join(i for i in block))

    return result


def get_type(delimiter:str):
    match delimiter:
        case "`":
            return TextType.CODE
        case "*":
            return TextType.ITALIC
        case "**":
            return TextType.BOLD
