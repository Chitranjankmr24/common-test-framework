from helpers.pbank_element_operations import click
from locators.admin_locator import admin_link, clean_db_btn


def clean_db():
    click(admin_link, "Admin Page")
    click(clean_db_btn, "Clean DB")
