import enum
import string
import random
from helpers.pbank_element_operations import *
from helpers.pbank_json_utils import *
from locators.user_registration_locator import *
u_name = ""


class Registration(enum.Enum):
    first_name = 'First Name:'
    last_name = 'Last Name:'
    address = 'Address:'
    city = 'City:'
    state = 'State:'
    zipcode = 'Zip Code:'
    phone = 'Phone #:'
    ssn = 'SSN:'
    user = 'Username:'
    password = 'Password:'
    confirm = 'Confirm:'


def create_new_user():
    click(registration_link, "Registration Link")
    type_text_with_replace_value(user_registration_textbox, Registration.first_name.value, get_data("first_name"),
                                 "First name")
    type_text_with_replace_value(user_registration_textbox, Registration.last_name.value, get_data("last_name"),
                                 "Last name")
    type_text_with_replace_value(user_registration_textbox, Registration.address.value,
                                 get_data("address"), "address")
    type_text_with_replace_value(user_registration_textbox, Registration.city.value, get_data("city"),
                                 "city")
    type_text_with_replace_value(user_registration_textbox, Registration.state.value, get_data("state"),
                                 "State")
    type_text_with_replace_value(user_registration_textbox, Registration.zipcode.value, get_data("zipcode"),
                                 "zipcode")
    type_text_with_replace_value(user_registration_textbox, Registration.phone.value, get_data("phone"),
                                 "Phone")
    type_text_with_replace_value(user_registration_textbox, Registration.ssn.value, get_data("ssn"),
                                 "SSN")
    type_text_with_replace_value(user_registration_textbox, Registration.user.value, get_data("user"),
                                 "User")
    type_text_with_replace_value(user_registration_textbox, Registration.password.value, get_data("password"),
                                 "Password")
    type_text_with_replace_value(user_registration_textbox, Registration.confirm.value, get_data("confirm"),
                                 "Confirm")
    click(register_btn, "REGISTER")


def generate_user():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))


