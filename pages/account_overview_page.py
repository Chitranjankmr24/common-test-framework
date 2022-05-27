import time

from helpers.pbank_element_operations import click, get_element_text
from locators.account_overview_locator import *


def get_acc_number():
    click(acc_overview_link, "Account OverView")
    return get_element_text(acc_number_text)


def get_total_amount():
    click(acc_overview_link, "Account OverView")
    time.sleep(1)
    return get_element_text(total_amount)
