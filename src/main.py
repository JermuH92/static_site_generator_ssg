import os
import shutil
from page_generator import generate_pages_recursive


def copy_static_recursive(source_path, destination_path):

    items = os.listdir(source_path)

    for item in items:

        full_source_path = os.path.join(source_path, item)
        full_destination_path = os.path.join(destination_path, item)

        if os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_destination_path)
            print(f"Copied file: {full_source_path} -> {full_destination_path}")
        
        elif os.path.isdir(full_source_path):
            os.mkdir(full_destination_path)
            print(f"Created a directory: {full_destination_path}")

            copy_static_recursive(full_source_path, full_destination_path)


def main():

    source_dir = "static"
    destination_dir = "public"

    print("Cleaning public folder...")

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)

    print("Beginning recursive copying of static files...")
    copy_static_recursive(source_dir, destination_dir)
    print("Copying complete.")

    print("Generating pages...")
    generate_pages_recursive("content", "template.html", "public")
    

if __name__ == "__main__":
    main()