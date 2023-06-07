import config
from shutil import rmtree
import re, os, sys, time, datetime
import glob as g
import frontmatter
from enum import Enum

import argparse

class PostStatus(Enum):
    IS_DRAFT = 1
    IS_NOT_DRAFT = 2
    DRAFT_YAML_KEY_DOESNT_EXIST = -1

class Obsidian_to_Hugo:

    def __init__(self):
        self.markdown_files = []
        self.number_of_posts_copied_over = 0

    def remove_existing_hugo_posts(self):
        try:
            rmtree(config.hugo_posts_path)
        except: pass
    
    def recreate_hugo_folders(self):
        # adds the folder back as it's deleted above
        os.makedirs(config.hugo_posts_path)
        os.makedirs(config.hugo_drafts_path)

    def find_all_markdown_files_in_obsidian(self):
        for folder in config.obsidian_blog_folders:
            path = config.obsidian_vault_path + "/" + folder
            # print(path)
            return g.glob(path + "/*.md")

    def _replace_links_with_hugo_syntax(self, match_obj):
        if match_obj.group(1) is not None:
            link = match_obj.group(1).replace("[[", "").replace("]]", "")
            # print(match_obj.group())

            if link.find("|") >= 0:
                link_text = link.split("|", 1)
                return '[' + link_text[1].strip() + ']({{< ref "' + link_text[0].strip() +'" >}})'
            
            return '{{< ref "' + link + '" >}}'

    def _replace_links(self, filedata) -> str:
        return re.sub(r"(\[\[.+?\]\])", self._replace_links_with_hugo_syntax, filedata)

    def _is_post_a_draft(self, filedata) -> PostStatus:
        # load the yaml frontmatter
        yaml = frontmatter.loads(filedata)
        # print(yaml.keys())

        try:
            if yaml["draft"]:
                return PostStatus.IS_DRAFT
        except KeyError:
            return PostStatus.DRAFT_YAML_KEY_DOESNT_EXIST
        
        return PostStatus.IS_NOT_DRAFT

    def _copy_draft_over_to_hugo(self, filedata, file_path):
        with open(config.hugo_drafts_path + "/" + os.path.basename(file_path), 'w') as file:
            file.write(filedata)
            self.number_of_posts_copied_over += 1

    def replace_links_in_files_and_copy_files_to_hugo(self, markdown_files):
        for file_path in markdown_files:
            # Read in the file
            with open(file_path, 'r') as file:
                filedata = file.read()

            # Replace the target string
            filedata = self._replace_links(filedata)

            draft_status = self._is_post_a_draft(filedata)

            if draft_status == PostStatus.IS_DRAFT:
                # check if blog post is still a draft, if it is, move it into draft folder in Hugo
                self._copy_draft_over_to_hugo(filedata, file_path)
                continue

            if draft_status == PostStatus.DRAFT_YAML_KEY_DOESNT_EXIST:
                print("WARNING: post doesn't have 'draft' frontmatter key, post treated as published by Hugo: " + file_path)
                sys.stdout.flush() # so print() works on git bash

            # Write the file out again
            with open(config.hugo_posts_path + "/" + os.path.basename(file_path), 'w') as file:
                file.write(filedata)
                self.number_of_posts_copied_over += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Obsidian to Hugo',
                    description='Copies over Obsidian .md files to Hugo.',
                    epilog='Look at README for more info')

    parser.add_argument('-w', '--watch', nargs="?", const=True, default=False,
                        help="Copies over everything but then watches for changes (when watching does not delete files in Hugo, only replaces ones that change)")
    args = parser.parse_args()

    obsidian_to_hugo = Obsidian_to_Hugo()
    markdown_files = []

    obsidian_to_hugo.remove_existing_hugo_posts()

    obsidian_to_hugo.recreate_hugo_folders()

    markdown_files = obsidian_to_hugo.find_all_markdown_files_in_obsidian()

    obsidian_to_hugo.replace_links_in_files_and_copy_files_to_hugo(markdown_files)

    print(f'Posts successfully copied over to Hugo: {str(obsidian_to_hugo.number_of_posts_copied_over)}')
    sys.stdout.flush() # so print() works on git bash

    if args.watch:
        print("Watching for changes...")
        sys.stdout.flush() # so print() works on git bash

        print("Press Ctrl C to quit")
        sys.stdout.flush() # so print() works on git bash

        time_to_compare_to = time.time()
        while True:
            obsidian_to_hugo.number_of_posts_copied_over = 0

            markdown_files = obsidian_to_hugo.find_all_markdown_files_in_obsidian()
            time_checked = datetime.datetime.now().strftime("%H:%M:%S")

            modified_markdown_files = []

            for file in markdown_files:
                file_mod_time = os.path.getmtime(file)
                if file_mod_time > time_to_compare_to:
                    modified_markdown_files.append(file)
            
            if len(modified_markdown_files) > 0:
                obsidian_to_hugo.replace_links_in_files_and_copy_files_to_hugo(modified_markdown_files)

                print(f'{time_checked} | {str(obsidian_to_hugo.number_of_posts_copied_over)} post(s) copied over to Hugo')
                sys.stdout.flush() # so print() works on git bash


            time_to_compare_to = time.time()
            time.sleep(10)
