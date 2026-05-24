import os
import pathlib
from markdown_blocks import (
    markdown_to_html_node,
    extract_title
)

def generate_pages_recursive(directory_path_content, template_path, destination_dir_path):

    entries = os.listdir(directory_path_content)

    for entry in entries:
        full_src_path = os.path.join(directory_path_content, entry)
        full_dest_path = os.path.join(destination_dir_path, entry)

        if os.path.isdir(full_src_path):
            os.mkdir(full_dest_path)

            generate_pages_recursive(full_src_path, template_path, full_dest_path)
        
        elif os.path.isfile(full_src_path):
            if full_src_path.endswith(".md"):
                new_path = pathlib.Path(full_dest_path).with_suffix(".html")

                generate_page(full_src_path, template_path, new_path)
                

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
    
    with open(template_path, "r") as template_file:
        template = template_file.read()
    
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_replace = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as destination_file:
        destination_file.write(template_replace)


