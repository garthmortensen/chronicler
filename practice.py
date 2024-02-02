import logging
import os
import inspect


def config_logs():

    # define logging directory
    home = os.path.expanduser("~")
    log_dir = os.path.join(home, "chronicler_logs")

    # dont overwrite existing log files
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # get calling script
    calling_script = inspect.stack()[1]

    # define log file name
    file_name = os.path.basename(calling_script.filename)
    filename_wo_extension = os.path.splitext(file_name)[0]
    log_file = os.path.join(log_dir, f"{filename_wo_extension}.log")

    log_format = "%(asctime)s %(filename)s:%(lineno)d %(funcName)s| %(message)s"

    handlers=[  # write stdout and errout
        logging.FileHandler(filename=log_file, mode="w"),  # writes to file
        logging.StreamHandler()  # streams to console
    ]

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=handlers
    )

def hello_world():
    config_logs()
    logging.info("Hello, world!")
    print("its nice")

def hello_world_logger():
    """function can be imported into another script and when called, will log 'Hello, world!'"""
    logging.info("Hello, world!")

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
