from textnode import *
from htmlnode import *
from markdownprocessing import *
from fileprocessing import *
import sys

def main():
    args = sys.argv
    if len(args) <= 1:
        basepath = "/"
    else:
        basepath = args[1]
    print(f"Starting the script with a basepath: {basepath}")
    generate_files("docs", "static")
    generate_pages_recursive("content", "template.html", "docs", basepath)
main()
