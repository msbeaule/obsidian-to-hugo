# Obsidian to Hugo

Finds all markdown files in specified Obsidian folders and converts links to the Hugo link syntax, then copies over the files into specified Hugo posts/blog folder.

## Run it

1. Make a copy of `config-example.py` and rename it to `config.py`, and add your obsidian vault path, the folders inside the obsidian vault you want to move over to hugo, and the hugo posts path
2. Run `python main.py`

## Run tests

Use `pytest` or `pytest -q` to run tests.
