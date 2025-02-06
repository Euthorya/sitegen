from textnode import TextNode, TextType


def main():
    node = TextNode("text", TextType.BOLD, "url")
    print(node)

main()