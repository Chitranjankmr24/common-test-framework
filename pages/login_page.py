from helpers.pbank_driver_manager import logger, load_url
from helpers.pbank_element_operations import type_text, click
from helpers.pbank_element_validation import is_element_present
from helpers.pbank_env import browser
from locators.login_locator import user_textbox, pwd_textbox, login_btn, logout_btn


def log_into_app(server_url, username, password):
    logger.info("---------------------Login to the Application---------------------\n")
    load_url(server_url)
    if is_element_present(user_textbox, "username"):
        type_text(user_textbox, username, "username")
        type_text(pwd_textbox, password, "username")
        click(login_btn, "LOG IN")


def logout():
    click(logout_btn, "Log Out")


def load_base_page(server_url):
    load_url(server_url)
