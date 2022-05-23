import os
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager

from helpers.pbank_env import browser, browser_mode
from helpers.pbank_system_properties import current_os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import logging

logger = logging.getLogger(__name__)

driver = None
wait = None


class WaitForDocReady(object):
    def __call__(self, driver):
        page_state = driver.execute_script('return document.readyState;')
        return page_state == "complete"


class WaitForJQuery(object):

    def __call__(self, driver):
        return driver.execute_script("return jQuery.active") == 0


def wait_for_load(function):
    def wait_check_js(*args, **kwargs):
        wait.until(WaitForDocReady())
        value = function(*args, **kwargs)
        return value

    return wait_check_js


def create_driver():
    web_driver = None
    browser_type = browser.lower()
    if os.environ.get("Browser"):
        browser_type = os.environ.get("Browser").lower()
    if browser_type == "firefox":
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_preference("dom.disable_beforeunload", True)
        web_driver = webdriver.Firefox(GeckoDriverManager().install(), options=firefox_options,
                                       desired_capabilities=cap)
    elif browser_type == "chrome":
        chrome_options = set_chrome_options()
        capabilities = webdriver.DesiredCapabilities.CHROME
        if browser_mode == "headless":
            chrome_options.headless = True
            chrome_options.add_argument("--window-size=1920,1080")
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        web_driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                                      desired_capabilities=capabilities)

    elif browser_type == "ie":
        cap = DesiredCapabilities.INTERNETEXPLORER
        cap["NATIVE_EVENTS"] = False
        web_driver = webdriver.Ie(IEDriverManager.install(), capabilities=cap)
    return web_driver


def create_wait():
    web_driver_wait = WebDriverWait(driver, 2)
    return web_driver_wait


class create_driver_instance:

    def get_driver(self):
        global driver
        if not driver:
            driver = create_driver()
        return driver

    def get_wait(self):
        global wait
        if not wait:
            wait = create_wait()
        return wait


def capture_screenshot(image_name):
    driver.get_screenshot_as_file(image_name)


def kill_driver_instance():
    global driver
    driver.quit()


def create_action_chains():
    return ActionChains(driver)


def load_url(app_url):
    driver.get("https://" + app_url)
    logger.info(f"Load URL: https://{app_url}")
    driver.maximize_window()


def reload_url(app_url):
    logger.info("RELOADING TO BASE PAGE: " + app_url)
    driver.get(app_url)
    driver.maximize_window()


def get_current_url():
    return driver.current_url


def set_chrome_options():
    options = webdriver.ChromeOptions()
    if current_os == "Linux":
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument('ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    preferences = {
        "profile.default_content_setting_values.automatic_downloads": 1,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", preferences)
    return options


def set_firefox_preferences():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 4)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    profile.update_preferences()
    return profile


def delete_cookies():
    send_command = ('POST', '/session/$sessionId/chromium/send_command')
    driver.command_executor._commands['SEND_COMMAND'] = send_command
    driver.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCookies', params={}))
