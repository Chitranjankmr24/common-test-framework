from helpers.pbank_base_locator import *

open_new_acc_link = (xpath, "//a[normalize-space()='Open New Account']")
select_acc_type = (xpath, "//select[@id='type']")
select_acc_no_dropdown = (xpath, "//select[@id='fromAccountId']")
open_account_btn = (css, "input[value='Open New Account']")
open_acc_msg = (xpath, "//p[normalize-space()='Congratulations, your account is now open.']")
acc_no_msg = (xpath, "//b[normalize-space()='Your new account number:']")
