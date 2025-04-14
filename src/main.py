from textnode import *
from htmlnode import *
from markdownprocessing import *
from fileprocessing import *

def main():
    generate_files()
    generate_pages_recursive("content", "template.html", "public")
main()
