# Obsidian to Hugo

Finds all markdown files in specified Obsidian folders and converts links to the Hugo link syntax, then copies over the files into specified Hugo posts/blog folder.

**WARNING:** Whatever path you set for the posts folder in Hugo will be deleted and remade every time you run the script.

## Run it

1. Make a copy of `config-example.py` and rename it to `config.py`, and add your Obsidian vault path, the folders inside the Obsidian vault you want to move over to Hugo, and the Hugo posts/blog path
2. Run `python main.py`

## Run tests

Use `pytest` or `pytest -q` to run tests.

The code block test should be the only one failing.

## Todo

- [ ] change it so \[\[text\]\] inside a code block (with the triple backticks) doesn't get converted to a link
- [ ] create an optional setting: check the `date` yaml key in each post to see if it's today's date or earlier, otherwise it won't copy over
- [ ] be able to add obsidian folders to check for images, and if a local image link is found in a post, copy over the image to Hugo and update the image link