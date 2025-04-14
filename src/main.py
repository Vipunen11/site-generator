from textnode import *
from htmlnode import *
from markdownprocessing import *
from fileprocessing import *

def main():
    generate_files()
    generate_page("content/index.md", "template.html", "public/index.html")
main()
