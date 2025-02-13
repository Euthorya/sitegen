from htmlnode import LeafNode
from textnode import TextNode, TextType
from static import copy_static, generate_page, generate_pages_recursive


def main():
    copy_static()
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content/", "template.html", "public/")
main()