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
                new_directory = os.path.join(directory, filepath)
                new_public_directory = os.path.join(public_directory, filepath)
                print(f"Making directory {new_public_directory}")
                os.mkdir(new_public_directory)
                recursive_copy(new_directory, new_public_directory)
    return recursive_copy(directory, public_directory)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating html page from markdown at {from_path} to {dest_path} using {template_path}")
    with open(template_path, 'r') as file:
        template = file.read()
    with open(from_path, 'r') as file:
        markdown = file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    title_inserted = template.replace("{{ Title }}", title)
    content_inserted = title_inserted.replace("{{ Content }}", content)
    with open(dest_path, 'x') as file:
        file.write(content_inserted)

def generate_pages_recursive(from_path, template_path, dest_path):
    dir_list = os.listdir(from_path)
    for filepath in dir_list:
        if os.path.isfile(os.path.join(from_path, filepath)):
            if filepath[-3:] == ".md":
                generate_page(os.path.join(from_path, filepath), template_path, f"{os.path.join(dest_path, filepath)[:-2]}html")
        else:
            new_from_path = os.path.join(from_path, filepath)
            new_dest_path = os.path.join(dest_path, filepath)
            if os.path.exists(new_dest_path) == False:
                print(f"Making directory {new_dest_path}")
                os.mkdir(new_dest_path)
            generate_pages_recursive(new_from_path, template_path, new_dest_path)

