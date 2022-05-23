from helpers.pbank_base_locator import *

registration_link = (xpath, "//a[normalize-space()='Register']")
user_registration_textbox = (xpath, "//td[b[text()='{}']]//following-sibling::td//input")
register_btn = (css, "input[value='Register']")
registration_msg = (css, "div[id='rightPanel'] p")

