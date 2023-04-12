import config
from shutil import rmtree
import re
import glob as g
import os

markdown_files = []

def remove_exists_hugo_posts():
    try:
        rmtree(config.hugo_posts_path)
    except: pass
    # adds the folder back as it's deleted above
    os.makedirs(config.hugo_posts_path)

def find_all_markdown_files_in_obsidian():
    for folder in config.obsidian_blog_folders:
        path = config.obsidian_vault_path + "/" + folder
        # print(path)
        markdown_files.extend(g.glob(path + "/*.md"))

def _replace_links_with_hugo_syntax(match_obj):
    if match_obj.group(1) is not None:
        link = match_obj.group(1).replace("[[", "").replace("]]", "")
        # print(match_obj.group())

        if link.find("|") >= 0:
            link_text = link.split("|", 1)
            return '[' + link_text[1].strip() + ']({{< ref "' + link_text[0].strip() +'" >}})'
        
        return '{{< ref "' + link + '" >}}'

def replace_links(filedata) -> str:
    return re.sub(r"(\[\[.+?\]\])", _replace_links_with_hugo_syntax, filedata)

def replace_links_in_files_and_copy_files_to_hugo():
    for file_path in markdown_files:
        # Read in the file
        with open(file_path, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = replace_links(filedata)

        # Write the file out again
        with open(config.hugo_posts_path + "/" + os.path.basename(file_path), 'w') as file:
            file.write(filedata)

remove_exists_hugo_posts()

find_all_markdown_files_in_obsidian()
# print(markdown_files)

replace_links_in_files_and_copy_files_to_hugo()
