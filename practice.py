import os
import logging
import platform
import getpass
import time  # timestamp, timers and sleep


def log_conf(invoking_filename):
    # logging in home dir seems like secure programming
    log_dir = os.path.join(os.path.expanduser("~"), "chronicles")
    if not os.path.exists(log_dir):
        print(f"mkdir for logs: {log_dir}")
        os.makedirs(log_dir)

    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())

    # this module is meant to be imported and log info about the calling script
    # use calling script name for log filename
    filename_wo_extension = os.path.splitext(invoking_filename)[0]  # remove .py
    log_file = os.path.join(log_dir, f"{timestamp}_{filename_wo_extension}.log")

    log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s| %(message)s"

    handlers=[  # write stdout and errout
        logging.StreamHandler(),  # stream to console
        logging.FileHandler(filename=log_file, mode="w")  # write to file
    ]

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y%m%d_%H%M%S",
        handlers=handlers
    )

    logging.info(f"log:    {log_file}")


def log_meta(invoking_file_dir, invoking_filename):
    # meta info to log
    os_version = platform.platform()
    python_version = platform.python_version()
    whoami = getpass.getuser()
    pid = os.getpid()

    # ascii art dividers: determine if os or file string is longer, and remove padding for "key"
    half_separator = int(max(len(os_version), len(invoking_filename)) / 2) - len("OS: ")
    top_separator = "✧" + "-" * half_separator + " meta info " + "-" * half_separator + "✧"  # ╔═══ META INFO ═══╗
    bottom_separator = "✧" + "-" * (len(top_separator) - 2) + "✧"  # ╚════════╝

    logging.info(f"dir:    {invoking_file_dir}")
    logging.info(f"file:   {invoking_filename}")
    logging.info(f"whoami: {whoami}")
    logging.info(f"python: {python_version}")
    logging.info(f"os:     {os_version}")
    logging.info(f"pid:    {pid}")

def log_init(invoking_file_dir, invoking_filename):  # all 8 letters for aligned console output
    log_conf(invoking_filename)
    log_meta(invoking_file_dir, invoking_filename)




