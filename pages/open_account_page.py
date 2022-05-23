import time

from helpers.pbank_element_operations import *
from locators.open_account_locator import *


def click_open_new_account():
    click(open_new_acc_link, "Open account")


def select_account_type(account_type):
    select_dropdown_value(select_acc_type, account_type)


def select_account_no(account_no):
    select_dropdown_value(select_acc_no_dropdown, account_no)


def click_open_account():
    click(open_account_btn, "Open Account Button")
