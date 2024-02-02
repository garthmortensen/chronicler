import os
import logging
import platform
import getpass
import time  # timestamp, timers and sleep
import subprocess  # for git info


def log_conf(invoking_filename: str) -> str:
    """Configure logging for the calling script.
    Sets up logs to write to a file in the user's home directory and print to console.    
    Return the log file path.
    """

    # logging in home dir seems like secure programming
    log_dir = os.path.join(os.path.expanduser("~"), "chronicles")
    if not os.path.exists(log_dir):
        print(f"mkdir for logs: {log_dir}")
        os.makedirs(log_dir)

    # this module is meant to be imported and log info about the calling script
    # use calling script name for log filename; include timestamp for uniqueness.
    # But if script is run multiple times per second, only the last log remains.
    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    filename_wo_extension = os.path.splitext(invoking_filename)[0]  # remove .py
    log_file = os.path.join(log_dir, f"{timestamp}_{filename_wo_extension}.log")

    handlers=[  # write stdout and errout
        logging.StreamHandler(),  # stream to console
        logging.FileHandler(filename=log_file, mode="w")  # write to file
    ]

    # 20240202_154449 INFO practice.py:56 log_meta| pid:    10629
    log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s| %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y%m%d_%H%M%S",
        handlers=handlers
    )

    return log_file


def log_meta(invoking_file_dir: str, invoking_filename: str, log_file: str):
    """Log meta information about the calling script, environmental variables, and git info."""

    # meta info to log
    os_version = platform.platform()
    python_version = platform.python_version()
    whoami = getpass.getuser()
    pid = os.getpid()

    # ascii art dividers: determine if os or file string is longer, and remove padding for "key"
    half_length = 25
    separator_head = "✧" + "-" * half_length + " meta log { " + "-" * half_length + "✧"  # ╔═══ meta log { ═══╗
    separator_foot = "✧" + "-" * half_length + " meta log } " + "-" * half_length + "✧"  # ╔═══ meta log } ═══╗

    logging.info(separator_head)
    logging.info(f"log:    {log_file}")
    logging.info(f"dir:    {invoking_file_dir}")
    logging.info(f"file:   {invoking_filename}")
    logging.info(f"whoami: {whoami}")
    logging.info(f"python: {python_version}")
    logging.info(f"os:     {os_version}")
    logging.info(f"pid:    {pid}")

    # get available git info
    try:  # repo may only be local
        git_origin_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode("utf-8").strip()
        logging.info(f"url:    {git_origin_url}")
    except subprocess.CalledProcessError:
        logging.warning("git url unavailable")

    try:  # if no .git, no branch
        git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
        logging.info(f"branch: {git_branch}")
    except subprocess.CalledProcessError:
        logging.warning("git branch unavailable")

    try:  # after git init, no commits yet
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        logging.info(f"hash:   {git_hash[:7]}")  # 8 chars per https://stackoverflow.com/a/18134919
    except subprocess.CalledProcessError:
        logging.warning("git hash unavailable")

    try:  # get commit message header
        git_commit_message = subprocess.check_output(["git", "log", "-1", "--pretty=%s"]).decode("utf-8").strip()
        logging.info(f"commit: {git_commit_message}")
    except subprocess.CalledProcessError:
        logging.warning("git commit message unavailable")

    logging.info(separator_foot)


def log_init(invoking_file_dir: str, invoking_filename: str):  # all 8 letters for aligned console output
    """Initialize logging for the calling script.
    Takes as input the directory and filename of the calling script."""
    log_file = log_conf(invoking_filename)
    log_meta(invoking_file_dir, invoking_filename, log_file)
