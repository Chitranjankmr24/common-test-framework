from helpers.pbank_element_operations import type_text, click
from helpers.pbank_json_utils import get_data
from locators.request_loan_locator import *


def click_request_loan():
    click(request_loan_link, "Request Loan")


def request_loan():
    type_text(loan_amount_text, get_data("loan_amount"), "Loan Amount")
    type_text(down_payment_text, get_data("down_payment"), "Down Payment")
    click(apply_now_btn, "Apply Now")
