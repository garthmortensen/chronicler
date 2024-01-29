import logging
import subprocess
import time
import platform  # get OS and Python version
import getpass  # get username
import os # get dir
import datetime  # format datetime
import yaml  # read yaml log config

date_format = "%Y%m%d_%H%M%S"  # compact ISO 8601, less T
start_time = time.time()

log_format = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d - %(funcName)s()]: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)

def read_log_config(log_config_filepath):
    with open(log_config_filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config

def log_meta_info(start_time, log_config):
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime(date_format)  # somewhat redundant
    os_version = platform.platform()
    python_version = platform.python_version()
    whoami = getpass.getuser()
    file_name = __file__
    file_dir = os.path.dirname(os.path.abspath(file_name))
    pid = os.getpid()

    # ascii art dividers: determine if os or file string is longer, and remove padding for "key"
    half_separator = int(max(len(os_version), len(file_name)) / 2) - len("OS: ")
    top_separator = "✧" + "-" * half_separator + " meta info " + "-" * half_separator + "✧"  # ╔═══ META INFO ═══╗
    bottom_separator = "✧" + "-" * (len(top_separator) - 2) + "✧"  # ╚════════╝

    logging.info(top_separator)
    logging.info(f"start:  {start_time_str}")
    logging.info(f"whoami: {whoami}")
    logging.info(f"py ver: {python_version}")
    logging.info(f"file:   {file_name}")
    logging.info(f"dir:    {file_dir}")
    logging.info(f"os:     {os_version}")
    logging.info(f"pid:    {pid}")

    # git info (if available)
    try:  # if no .git, no branch
        git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
        logging.info(f"branch: {git_branch}")
    except subprocess.CalledProcessError:
        logging.warning("git branch unavailable")

    try:  # after git init, no commits yet
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        logging.info(f"hash:   {git_hash}")
    except subprocess.CalledProcessError:
        logging.warning("git hash unavailable")

    try:
        git_origin_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode("utf-8").strip()
        logging.info(f"url:    {git_origin_url}")
    except subprocess.CalledProcessError:
        logging.warning("git url unavailable")

    logging.info(bottom_separator)

def hello_world():
    logging.info("Hello, world!")

def my_function():
    logging.info("This is an info message")

def log_total_runtime(start_time):
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total runtime: {total_time:.2f} seconds")


log_config = read_log_config("log_config.yaml")
log_meta_info(start_time, log_config)
hello_world()
my_function()
log_total_runtime(start_time)
