import os, shutil
import logging

from markdown import markdown_to_html_node
from markdown_blocks import extract_header
logger = logging.getLogger(__name__)

PUBLIC_PATH = "./public/"
STATIC_PATH = "./static/"
PAGE_NAME = "index.html"


def copy_static():
    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)
    os.mkdir(PUBLIC_PATH)
    copy_dir(STATIC_PATH, PUBLIC_PATH)
    return True

def copy_dir(directory:str, destination:str):
    contents = os.listdir(directory)
    for content in contents:
        path = directory + content
        if not os.path.isfile(path):
            path += "/"
            folder = destination + content + "/"
            os.mkdir(folder)
            copy_dir(path, folder)
        else:
            shutil.copy(path, destination)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown, template = (read_file(i) for i in [from_path, template_path])
    html = markdown_to_html_node(markdown).to_html()
    title = extract_header(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_directory = "".join(dest_path.split("/")[:-1])
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    with open(dest_path, "w") as f:
        f.write(template)
    
def read_file(path):
    with open(path) as f:
        return f.read()
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for content in contents:
        print(f"Generating path: {content}")
        path = os.path.join(dir_path_content, content)
        destination = os.path.join(dest_dir_path, content)
        if not os.path.isfile(path):
            if not os.path.exists(destination):
                os.makedirs(destination)
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, content))
        else:
            html_content = f"{content.split('.')[0]}.html"
            generate_page(os.path.join(dir_path_content, content), template_path, os.path.join(dest_dir_path, html_content))

