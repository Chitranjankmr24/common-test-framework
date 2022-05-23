from helpers.pbank_base_locator import *

request_loan_link = (xpath, "//a[normalize-space()='Request Loan']")
loan_amount_text = (css, "#amount")
down_payment_text = (css, "#downPayment")
apply_now_btn = (css, "input[value='Apply Now']")
request_loan_msg = (xpath, "//p[normalize-space()='Congratulations, your loan has been approved.']")
