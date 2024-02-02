import logging
from chronicler import log_init
from pathlib import Path


def get_script_path_and_file():
    this_dir = str(Path(__file__).parent)
    this_file = str(Path(__file__).name)
    return this_dir, this_file

def hello_world():
    logging.info("Hello, world!")

this_dir, this_file = get_script_path_and_file()
log_init(this_dir, this_file)

hello_world()
