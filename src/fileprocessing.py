import os
import shutil
from textnode import *
from htmlnode import *
from markdownprocessing import *

def generate_files():
    shutil.rmtree('public')
    os.mkdir('public')
    public_directory = "public"
    directory = "static"
    def recursive_copy(directory, public_directory):
        dir_list = os.listdir(directory)
        for filepath in dir_list:
            if os.path.isfile(os.path.join(directory, filepath)):
                print(f"Copying file {os.path.join(public_directory, filepath)}")
                shutil.copy(os.path.join(directory, filepath), os.path.join(public_directory, filepath))
            else:
                directory = os.path.join(directory, filepath)
                public_directory = os.path.join(public_directory, filepath)
                print(f"making directory {public_directory}")
                os.mkdir(public_directory)
                recursive_copy(directory, public_directory)
    return recursive_copy(directory, public_directory)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")
    with open(template_path, 'r') as file:
        template = file.read()
    with open(from_path, 'r') as file:
        markdown = file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    title_inserted = template.replace("{ Title }}", title)
    content_inserted = title_inserted.replace("{{ Content }}", content)
    with open(dest_path, 'x') as file:
        file.write(content_inserted)
