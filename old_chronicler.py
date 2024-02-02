import logging
import subprocess
import time
import platform  # get OS and Python version
import getpass  # get username
import os # get dir
import datetime  # format datetime
import yaml  # read yaml log config
import inspect # get calling script

# TODO: this is dumb. refactor somehow: new file created
# TODO: make this importable: new file created
# TODO: OOP?
date_format = "%Y%m%d_%H%M%S"  # compact ISO 8601, less T
start_time = time.time()

def define_start_time(date_format):
    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime(date_format)
    return start_time_str

def config_logs(date_format):
    start_time_str = define_start_time(date_format)

    # define logging directory
    home = os.path.expanduser("~")
    log_dir = os.path.join(home, "chronicler_logs")

    # dont overwrite existing log files
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # define log file name
    filename = os.path.basename(__file__)
    filename_wo_extension = os.path.splitext(filename)[0]
    log_file = os.path.join(log_dir, f"{start_time_str}_{filename_wo_extension}.log")

    log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s| %(message)s"

    handlers=[  # write stdout and errout
        logging.FileHandler(filename=log_file, mode="w"),  # writes to file
        logging.StreamHandler()  # streams to console
    ]

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )

    return log_file


def parameterize_logs(log_config_filepath):
    with open(log_config_filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config


def log_header_info(log_config, log_file, date_format):
    start_time_str = define_start_time(date_format)
    os_version = platform.platform()
    python_version = platform.python_version()
    whoami = getpass.getuser()

    file_name = os.path.basename(__file__)
    file_dir = os.path.dirname(os.path.abspath(file_name))
    pid = os.getpid()

    # ascii art dividers: determine if os or file string is longer, and remove padding for "key"
    half_separator = int(max(len(os_version), len(file_name)) / 2) - len("OS: ")
    top_separator = "✧" + "-" * half_separator + " meta info " + "-" * half_separator + "✧"  # ╔═══ META INFO ═══╗
    bottom_separator = "✧" + "-" * (len(top_separator) - 2) + "✧"  # ╚════════╝

    logging.info(top_separator)
    if log_config.get('log_file'):
        logging.info(f"log file: {log_file}")
    if log_config.get('start_time'):
        logging.info(f"start:    {start_time_str}")
    if log_config.get('os_version'):
        logging.info(f"os:       {os_version}")
    if log_config.get('python_version'):
        logging.info(f"py ver:   {python_version}")
    if log_config.get('whoami'):
        logging.info(f"whoami:   {whoami}")
    if log_config.get('file_name'):
        logging.info(f"file:     {file_name}")
    if log_config.get('file_dir'):
        logging.info(f"dir:      {file_dir}")
    if log_config.get('pid'):
        logging.info(f"pid:      {pid}")

    # get available git info
    if log_config.get('git_info'):
        try:  # if no .git, no branch
            git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
            logging.info(f"branch:   {git_branch}")
        except subprocess.CalledProcessError:
            logging.warning("git branch unavailable")

        try:  # after git init, no commits yet
            git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
            logging.info(f"hash:     {git_hash[:7]}")  # 8 chars per https://stackoverflow.com/a/18134919
        except subprocess.CalledProcessError:
            logging.warning("git hash unavailable")

        try:  # repo may only be local
            git_origin_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode("utf-8").strip()
            logging.info(f"url:      {git_origin_url}")
        except subprocess.CalledProcessError:
            logging.warning("git url unavailable")

    logging.info(bottom_separator)


# do something like this
def setup_logging(script_name=None):
    log_file = config_logs(date_format)
    log_config = parameterize_logs("log_config.yaml")
    log_header_info(log_config, log_file, date_format)


def testing():
    # Get the filename and directory of the calling script
    calling_script = inspect.stack()[1]
    file_name = os.path.basename(calling_script.filename)
    file_dir = os.path.dirname(os.path.abspath(calling_script.filename))
    return file_name, file_dir


if __name__ == "__main__":
    setup_logging()
