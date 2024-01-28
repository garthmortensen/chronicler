import logging
import subprocess
import time
import platform  # get OS and Python version
import getpass  # get username

start_time = time.time()

log_format = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d - %(funcName)s()]: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y%m%d_%H%M%S")  # compact ISO 8601, less T

def log_system_info():
    os_version = platform.platform()
    python_version = platform.python_version()
    whoami = getpass.getuser()
    file_name = __file__
    # ascii art dividers: determine if os or file string is longer, and remove padding for 'key'
    half_separator = int(max(len(os_version), len(file_name)) / 2) - len("OS: ")
    top_separator = '✧' + '-' * half_separator + ' meta info ' + '-' * half_separator + '✧'  # ╔═══ META INFO ═══╗
    bottom_separator = '✧' + '-' * (len(top_separator) - 2) + '✧'  # ╚════════╝
    logging.info(top_separator)
    logging.info(f"whoami:     {whoami}")
    logging.info(f"py ver:     {python_version}")
    logging.info(f"file:       {file_name}")
    logging.info(f"os:         {os_version}")

    # git info (if available)
    try:  # if no .git, no branch
        git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
        logging.info(f"git branch: {git_branch}")
    except subprocess.CalledProcessError:
        logging.error("git branch info unavailable")
    try:  # after git init, no commits yet
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        logging.info(f"git hash:   {git_hash}")
    except subprocess.CalledProcessError:
        logging.error("git hash info unavailable")

    logging.info(bottom_separator)

def hello_world():
    logging.info("Hello, world!")

def my_function():
    logging.info("This is an info message")

def log_total_runtime(start_time):
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total runtime: {total_time:.2f} seconds")


log_system_info()
hello_world()
my_function()
log_total_runtime(start_time)
