import logging
import os
import inspect

def hello_world():
    logging.info("Hello, world!")
    print("its nice")

def print_file_name_of_calling_script():
    """function can be imported into another script and when called, will print the filename of the calling script"""
    calling_script = inspect.stack()[1]
    file_name = os.path.basename(calling_script.filename)
    print(file_name)

def print_directory_of_calling_script():
    """function can be imported into another script and when called, will print the directory of the calling script"""
    calling_script = inspect.stack()[1]
    file_dir = os.path.dirname(os.path.abspath(calling_script.filename))
    print(file_dir)
