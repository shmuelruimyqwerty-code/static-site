
import os
from spliter import markdown_to_html_node
import shutil

def extract_title(markdown_line):
    if markdown_line.startswith("# "):
        header = markdown_line[1:]
        return header.strip()
    else:
        raise Exception ("no header in md")

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using template_path")
    with open(from_path,encoding="utf-8") as f:
        whole_md = str(f.read())
    with open(template_path,encoding="utf-8") as t:
        template = str(t.read())
    html_nodes = markdown_to_html_node(whole_md)
    html_str = html_nodes.to_html()
    with open(from_path,encoding="utf-8") as f:
        f = list(f)
        head = f[0]
    title = extract_title(head)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)
    file_path = os.path.join(dest_path,"index.html")
    os.makedirs(dest_path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> None:
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        og_dir_path_content = dir_path_content
        og_dest_dir_path = dest_dir_path
        dir_path_content = os.path.join(dir_path_content, filename)
        dest_dir_path = os.path.join(dest_dir_path, filename)
        print(f" * {dir_path_content} -> {dest_dir_path}")
        if os.path.isfile(dir_path_content):
            generate_page(dir_path_content, template_path, og_dest_dir_path)
            dir_path_content = og_dir_path_content
            dest_dir_path = og_dest_dir_path
        else:
            generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
            dir_path_content = og_dir_path_content
            dest_dir_path = og_dest_dir_path
