

from page_gen import generate_page, generate_pages_recursive
from stat_to_pub import copy_files_recursive
import os
import shutil
import sys

dir_path_static = "./static"
dir_path_docs = "./docs"
if len(sys.argv) < 2:
    basepath = "/"
else:
    basepath = sys.argv[1]


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
