from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from helpers.pbank_driver_manager import logger, wait_for_load
from helpers.pbank_element_operations import wait, driver


@wait_for_load
def is_element_present(locator, elem_name, stop_on_fail=False):
    try:
        wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    except (NoSuchElementException, TimeoutException) as ex:
        logger.info(f"Element {elem_name} is not present")
        if stop_on_fail:
            raise ex
        return False
    logger.info(f"Element {elem_name} is present")
    return True


@wait_for_load
def is_element_present_replace_value(locator, value, stop_on_fail=False):
    if not type(value) is list: value = [value]
    logger.info(f"Checking element with value: '{value}' is present")
    try:
        wait.until(EC.visibility_of_element_located((locator[0], locator[1].format(*value))))
    except (NoSuchElementException, TimeoutException) as ex:
        logger.info(f"Element with value: '{value}' is not present")
        if stop_on_fail:
            raise ex
        return False
    logger.info(f"Element with value: '{value}' is present")
    return True


@wait_for_load
def check_element_exists(locator):
    try:
        wait.until(EC.element_to_be_clickable((locator[0], locator[1])))
    except (NoSuchElementException, TimeoutException) as error:
        logger.info(f"Element is not present on the page")
        return False
    return True


@wait_for_load
def is_checkbox_checked(locator, elem_name, replace_value=list()):
    if type(replace_value) != list: replace_value = [replace_value]
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1].format(*replace_value))))
    checked = elem.is_selected()
    if checked:
        logger.info(f'Element {elem_name} is checked')
    else:
        logger.info(f'Element {elem_name} is not checked')
    return checked


@wait_for_load
def is_element_clickable(locator, elem_name, stop_on_fail=False):
    try:
        wait.until(EC.element_to_be_clickable((locator[0], locator[1])))
    except (NoSuchElementException, TimeoutException) as ex:
        logger.info(f"Element {elem_name} is not clickable")
        if stop_on_fail:
            raise ex
        return False
    logger.info(f"Element {elem_name} is present and Clickable")
    return True
