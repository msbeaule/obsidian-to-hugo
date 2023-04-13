import config
from shutil import rmtree
import re
import glob as g
import os
import frontmatter

class Obsidian_to_Hugo:

    def __init__(self):
        self.markdown_files = []
        self.number_of_posts_copied_over = 0

    def remove_existing_hugo_posts(self):
        try:
            rmtree(config.hugo_posts_path)
        except: pass
        # adds the folder back as it's deleted above
        os.makedirs(config.hugo_posts_path)

    def find_all_markdown_files_in_obsidian(self):
        for folder in config.obsidian_blog_folders:
            path = config.obsidian_vault_path + "/" + folder
            # print(path)
            self.markdown_files.extend(g.glob(path + "/*.md"))

    def _replace_links_with_hugo_syntax(self, match_obj):
        if match_obj.group(1) is not None:
            link = match_obj.group(1).replace("[[", "").replace("]]", "")
            # print(match_obj.group())

            if link.find("|") >= 0:
                link_text = link.split("|", 1)
                return '[' + link_text[1].strip() + ']({{< ref "' + link_text[0].strip() +'" >}})'
            
            return '{{< ref "' + link + '" >}}'

    def replace_links(self, filedata) -> str:
        return re.sub(r"(\[\[.+?\]\])", self._replace_links_with_hugo_syntax, filedata)

    def replace_links_in_files_and_copy_files_to_hugo(self):
        for file_path in self.markdown_files:
            # Read in the file
            with open(file_path, 'r') as file:
                filedata = file.read()

            # load the yaml frontmatter
            yaml = frontmatter.loads(filedata)
            
            # check if blog post is still a draft, if it is skip over it and don't copy it over
            try:
                if yaml["draft"] is True:
                    continue
            except KeyError:
                print("ERROR: " + file_path + " doesn't have 'draft' yaml key, file not copied over")
                continue

            # Replace the target string
            filedata = self.replace_links(filedata)

            # Write the file out again
            with open(config.hugo_posts_path + "/" + os.path.basename(file_path), 'w') as file:
                file.write(filedata)
                self.number_of_posts_copied_over += 1

obsidian_to_hugo = Obsidian_to_Hugo()

obsidian_to_hugo.remove_existing_hugo_posts()

obsidian_to_hugo.find_all_markdown_files_in_obsidian()

obsidian_to_hugo.replace_links_in_files_and_copy_files_to_hugo()

print("Number of posts successfully copied over to Hugo: " + str(obsidian_to_hugo.number_of_posts_copied_over))
