# https://stackoverflow.com/a/20885799
from importlib import resources as impresources
from . import templates

def _read_template(basename: str) -> str:
    with ( impresources.files(templates) / basename ).open('rt') as f:
        return f.read()
