import time
from datetime import datetime
from selenium.webdriver.common.keys import *
from selenium.webdriver.support.select import Select
from helpers.pbank_driver_manager import *
from selenium.webdriver.support import expected_conditions as EC

driver = create_driver_instance().get_driver()
wait = create_driver_instance().get_wait()


@wait_for_load
def click(locator, elem_name):
    elem = wait.until(EC.element_to_be_clickable((locator[0], locator[1])))
    elem.click()
    logger.info(f"Clicked on {elem_name}")


@wait_for_load
def click_with_replace_value(locator, value, elem_name="button"):
    if not type(value) is list: value = [value]
    elem = wait.until(EC.element_to_be_clickable((locator[0], locator[1].format(*value))))
    elem.click()
    logger.info(f"Clicked on : {elem_name} with replace value: {value}")


@wait_for_load
def select_dropdown_value(locator, value, elem_name="dropdown"):
    elem = Select(wait.until(EC.visibility_of_element_located((locator[0], locator[1]))))
    elem.select_by_visible_text(value)
    time.sleep(1)
    logger.info(f"Clicked on : {elem_name} with replace value: {value}")


@wait_for_load
def scroll_element_into_view(locator):
    logger.info("Scrolling element into view")
    elem = wait.until(EC.presence_of_element_located((locator[0], locator[1])))
    driver.execute_script("arguments[0].scrollIntoView();", elem)


@wait_for_load
def actions_move_to_element(actions, locator):
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    actions.move_to_element(elem).perform()


@wait_for_load
def actions_move_element(actions, elem):
    actions.move_to_element(elem).perform()


@wait_for_load
def actions_move_to_element_and_click(actions, elem):
    actions.move_to_element(elem).click(elem).perform()


@wait_for_load
def actions_move_to_element_and_click_with_replace_value(actions, locator, value):
    if not type(value) is list: value = [value]
    elem = wait.until(EC.presence_of_element_located((locator[0], locator[1].format(*value))))
    actions.move_to_element(elem).click(elem).perform()


@wait_for_load
def get_element_text(locator):
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    logger.info(f"Text returned from element locator is {elem.text}")
    return elem.text


@wait_for_load
def type_text(locator, value, elem_name):
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    elem.clear()
    elem.send_keys(value)


@wait_for_load
def type_text_with_replace_value(locator, replace_string, value, elem_name):
    if not type(replace_string) is list: replace_string = [replace_string]
    logger.info(f"Type Value: {value} in: {elem_name} with replace: {replace_string}")
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1].format(*replace_string))))
    elem.clear()
    elem.send_keys(value)


@wait_for_load
def type_text_with_replace_value_and_enter(locator, replace_string, value, elem_name):
    if not type(replace_string) is list: replace_string = [replace_string]
    logger.info(f"Type Value: {value} in: {elem_name} with replace: {replace_string}")
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1].format(*replace_string))))
    elem.clear()
    elem.send_keys(value + Keys.ENTER)


@wait_for_load
def type_value_and_enter(locator, value, elem_name):
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    elem.clear()
    elem.send_keys(value + Keys.ENTER)
    logger.info(f"Entered text {value} in textbox {elem_name}")


@wait_for_load
def press_enter_key(locator, elem_name):
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    elem.send_keys(Keys.ENTER)
    logger.info(f"Pressing Enter in element {elem_name}")


@wait_for_load
def get_attribute_value(locator, attribute_name):
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    attribute_value = elem.get_attribute(attribute_name)
    logger.info(f"Attribute -> {attribute_name} | Value -> {attribute_value}")
    return attribute_value


@wait_for_load
def get_element(locator):
    elem = wait.until(EC.presence_of_element_located((locator[0], locator[1])))
    logger.info(f"Getting the reference of Webelement with locator : {locator}")
    return elem


@wait_for_load
def scroll_to_element_height(locator, num_of_time_to_scroll=1):
    logger.info("Scrolling element into view")
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    while num_of_time_to_scroll > 0:
        driver.execute_script("arguments[0].scrollTop=arguments[0].scrollTop + arguments[0].scrollHeight", elem)
        num_of_time_to_scroll = num_of_time_to_scroll - 1


@wait_for_load
def get_element_text_replace_value(locator, value, elem_name):
    if not type(value) is list: value = [value]
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1].format(*value))))
    actual_text = elem.text
    logger.info(f"Element: {elem_name} replaced with value: {value} has Text: {actual_text}")
    return actual_text


@wait_for_load
def get_elements_texts(locator):
    elems = wait.until(EC.presence_of_all_elements_located((locator[0], locator[1])))
    texts = []
    for elem in elems:
        texts.append(elem.text.strip())
    logger.info(f"Got texts: {texts}")
    return texts


@wait_for_load
def get_elements_attribute(locator, attribute_name):
    elems = wait.until(EC.visibility_of_all_elements_located((locator[0], locator[1])))
    values = []
    for elem in elems:
        values.append(elem.get_attribute(attribute_name))
    logger.info(f"Got attribute values for attribute {attribute_name}: {values}")
    return values


@wait_for_load
def get_visible_elements_texts(locator):
    elems = wait.until(EC.presence_of_all_elements_located((locator[0], locator[1])))
    texts = []
    for elem in elems:
        if elem.is_displayed():
            texts.append(elem.text)
    logger.info(f"Got texts: {texts}")
    return texts


@wait_for_load
def get_elements_texts_replace_value(locator, value):
    if not type(value) is list: value = [value]
    elems = wait.until(EC.visibility_of_all_elements_located((locator[0], locator[1].format(*value))))
    texts = []
    for elem in elems:
        texts.append(elem.text)
    logger.info(f"Got texts: {texts}")
    return texts


@wait_for_load
def mouse_over_click_using_offset(locator, x, y, elem_name):
    actions = create_action_chains()
    elem = wait.until(EC.element_to_be_clickable((locator[0], locator[1])))
    actions.move_to_element_with_offset(elem, x, y).click().perform()
    logger.info(f"Clicked on {elem_name} with offset x: {x} and y: {y}")


@wait_for_load
def mouse_over_click(locator):
    actions = create_action_chains()
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    actions.move_to_element(elem).click().perform()


@wait_for_load
def mouse_over_right_click(locator, elem_name):
    actions = create_action_chains()
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    actions.move_to_element(elem).context_click().perform()
    logger.info("Right clicked on " + elem_name)


@wait_for_load
def mouse_over(locator):
    actions = create_action_chains()
    elem = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
    actions.move_to_element(elem).perform()


@wait_for_load
def click_using_java_script(locator, elem_name):
    elem = wait.until(EC.visibility_of_any_elements_located((locator[0], locator[1])))
    driver.execute_script("arguments[0].click();", elem[0])
    time.sleep(1)
    logger.info(f"Clicked on {elem_name}")


def get_random_int(value):
    timestamp = datetime.now().strftime("%M%S%f")
    return f"{value}{timestamp}"
