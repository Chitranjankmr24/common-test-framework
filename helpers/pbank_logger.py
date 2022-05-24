import logging
import sys
from logging.handlers import RotatingFileHandler


class PBankLogger:
    def __init__(self, logger_file_name):
        self.logger = logger_file_name

    def get_logger(self, logger_file):
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
