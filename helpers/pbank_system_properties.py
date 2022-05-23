import os
import sys
import platform
from configparser import ConfigParser
from enum import Enum
from helpers.pbank_resources import root_folder

current_os = platform.system()

config = ConfigParser(comment_prefixes='/', allow_no_value=True)
if current_os == "Linux":
    config.read('config.ini')
else:
    config.read(os.path.join(root_folder, "config.ini"))


class SystemProperties(Enum):
    PBANK_URL = ('para-bank.url', '')
    PBANK_UNAME = ('para-bank.uname', '')
    PBANK_PASSWORD = ('para-bank.password', '')
    PBANK_BROWSER = ('para-bank.browser', '')
    PBANK_BROWSER_MODE = ('para-bank.browser_mode', '')
    PBANK_COLLECT_VIDEO = ('collect_video', '')
    PBANK_SLACK_WEBHOOK = ('para-bank.slack_webhook', '')
    PBANK_REGISTRATION = ('para-bank.registration', '')

    def __init__(self, property_name, default_value):
        self.property_name = property_name
        self.default_value = default_value

    def raw_value(self):
        try:
            return sys._xoptions[self.property_name]
        except KeyError:
            # check in config file
            return config['SystemProperties'].get(self.property_name, None)

    def value(self):
        rv = self.raw_value()
        return self.default_value if rv is None else rv

    def bool_value(self) -> bool:
        rv = self.raw_value()
        if rv and 'true' == rv:
            return True
        if rv and 'false' == rv:
            return False
        return bool(self.default_value)
