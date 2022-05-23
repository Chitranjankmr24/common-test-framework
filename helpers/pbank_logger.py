import logging
import os
import sys
import platform
from logging.handlers import RotatingFileHandler
from helpers.pbank_resources import root_folder, output_folder, \
    output_folder_name

current_os = platform.system()


class CBLogger:
    def __init__(self, logger_file_name):
        self.logger = logger_file_name

    @staticmethod
    def check_and_create_folder(folder_to_created):
        if current_os == "Linux":
            if not os.path.isdir(folder_to_created):
                os.makedirs(folder_to_created)
        else:
            if not os.path.isdir(os.path.join(root_folder, folder_to_created)):
                os.makedirs(os.path.join(root_folder, folder_to_created))

    @staticmethod
    def create_output_folder():
        CBLogger.check_and_create_folder(output_folder_name)

    def get_logger(self, logger_file):
        CBLogger.create_output_folder()
        logger = logging.getLogger("python.test.logger")
        logger.setLevel(logging.INFO)
        # logging format
        log_format = logging.Formatter('%(asctime)s.%(msecs)02d %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
                                       "%Y-%m-%d %H:%M:%S")

        # error and above to html report and console
        c_err_log = logging.StreamHandler(sys.stderr)
        c_err_log.setLevel(logging.ERROR)
        c_err_log.setFormatter(log_format)

        # info and above to html report
        c_log = logging.StreamHandler(sys.stdout)
        c_log.setLevel(logging.INFO)
        c_log.setFormatter(log_format)

        # info and above to file
        # rotating file handler - each of 1mb with maximum 5
        # 1mb = 1000000 bytes
        f_log = RotatingFileHandler(logger_file, maxBytes=1000000, backupCount=5)
        f_log.setLevel(logging.INFO)
        f_log.setFormatter(log_format)

        logger.addHandler(c_err_log)
        logger.addHandler(c_log)
        logger.addHandler(f_log)

        # avoiding captured log - will be duplicate of stdout
        logger.propagate = 0

        return logger
