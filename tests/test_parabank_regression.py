import pytest

from helpers.pbank_env import base_url, pwd
from helpers.pbank_json_utils import modify_parameter, get_data, set_data_path
from helpers.pbank_resources import testdata_folder
from locators.admin_locator import db_clean_msg
from locators.login_locator import welcome_user, user_textbox, pwd_textbox
from locators.request_loan_locator import request_loan_msg
from locators.user_registration_locator import registration_msg
from pages.account_overview_page import get_acc_number, get_total_amount
from pages.admin_page import clean_db
from pages.login_page import log_into_app, logout
from pages.open_account_page import *
from pages.request_loan_page import request_loan, click_request_loan
from pages.user_registration_page import create_new_user, generate_user
from helpers.pbank_element_operations import *
from helpers.pbank_element_validation import *

test_data_path = os.path.join(testdata_folder, "parabank_regression.json")
user_value = None


@pytest.fixture(scope="session", autouse=True)
def fixture_func():
    set_data_path(test_data_path)


@pytest.mark.order(1)
def test_register_new_user():
    """Register new user"""
    global user_value
    user_value = generate_user()
    modify_param = {'user': user_value, 'address': get_random_int(get_data("address"))}
    modify_parameter(modify_param)
    set_data_path(test_data_path)
    create_new_user()
    assert get_element_text(registration_msg) == "Your account was created successfully. You are now logged in."


@pytest.mark.depends(on=['test_register_new_user'])
def test_logout():
    """check logout feature"""
    logout()
    assert is_element_present(user_textbox, "username")
    assert is_element_present(pwd_textbox, "Password")


@pytest.mark.depends(on=['test_register_new_user'])
def test_verify_login():
    """check login feature"""
    global user_value
    log_into_app(base_url, user_value, pwd)
    assert get_element_text(welcome_user) in "Welcome " + f"{get_data('first_name')} {get_data('last_name')}"


def test_open_new_account():
    """Open new account"""
    acc_no = get_acc_number()
    click_open_new_account()
    select_account_type("SAVINGS")
    select_account_no(acc_no)
    click_open_account()
    assert is_element_present(open_acc_msg, "Open Account success") and is_element_present(acc_no_msg, "Account "
                                                                                                       "number "
                                                                                                       "generated")


def test_verify_total_amount():
    """Verify total amount"""
    get_total_amount()
    # assert is_element_present(request_loan_msg, "Request Loan success")


@pytest.mark.depends(on=['test_register_new_user'])
def test_request_loan():
    """Request for loan"""
    click_request_loan()
    request_loan()
    assert is_element_present(request_loan_msg, "Request Loan success")


@pytest.mark.order('last')
def test_db_clean():
    """Clean DB"""
    clean_db()
    assert get_element_text(db_clean_msg) == "Database Cleaned"
