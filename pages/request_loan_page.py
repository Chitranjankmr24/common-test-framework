from helpers.pbank_element_operations import type_text, click
from locators.request_loan_locator import *


def click_request_loan():
    click(request_loan_link, "Request Loan")


def request_loan():
    type_text(loan_amount_text, 500, "Loan Amount")
    type_text(down_payment_text, 100, "Down Payment")
    click(apply_now_btn, "Apply Now")
