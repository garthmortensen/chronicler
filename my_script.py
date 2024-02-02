from practice import log_init
import logging
from pathlib import Path


def get_script_path_and_file():
    this_dir = Path(__file__).parent
    this_file = Path(__file__).name
    return this_dir, this_file

this_dir, this_file = get_script_path_and_file()

log_init(this_dir, this_file)


def hello_world():
    logging.info("Hello, world!")

hello_world()
