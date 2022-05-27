import os.path
import pathlib
import threading

import pytest
import re

from helpers.pbank_check import soft_assert_failures_report
from helpers.pbank_driver_manager import logger, get_current_url, kill_driver_instance, \
    load_url
from helpers.pbank_element_operations import driver
from helpers.pbank_resources import screenshot_folder, screenrecorder_folder
from helpers.pbank_result_notification import *
from py._xmlgen import html
from datetime import datetime
import sys
from _pytest.runner import runtestprotocol

from helpers.pbank_screen_recorder import set_screencapture
from pages.login_page import load_base_page, log_into_app
from helpers.pbank_env import *

logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

sys.stdout = sys.stderr
server = None
test_name = ""
t_array = []
t1 = None
current_file = ""
outcome = None


@pytest.hookimpl
def pytest_runtest_setup(item):
    logging_plugin = item.config.pluginmanager.get_plugin("logging-plugin")
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d')
    timestamp_test = "_" + str(datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S'))
    logging_plugin.set_log_path(os.path.join('logs', timestamp, f'{item.name}' + timestamp_test + '.log'))


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    global outcome
    outcome = yield
    report = outcome.get_result()
    soft_assert_failures_report(report, call)
    extra = getattr(report, 'extra', [])
    setattr(item, "check_" + report.when, report)
    test_description = getattr(item.function, '__doc__', '')
    if not test_description:
        test_description = "Description is not provided for the Test"
    report.description = test_description
    if report.when == 'call' or report.when == 'setup':
        extra.append(pytest_html.extras.url(get_current_url()))
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = item.name + ".png"
            if not os.path.exists(screenshot_folder):
                os.makedirs(screenshot_folder)
            folder_name = create_folder(screenshot_folder)
            driver.save_screenshot(os.path.join(os.path.sep, screenshot_folder, folder_name, file_name))
            extra.append(pytest_html.extras.image(os.path.join(os.path.sep, screenshot_folder, folder_name, file_name)))
        report.extra = extra


def pytest_html_report_title(report):
    report.title = "Para Bank Automation Execution Report"


@pytest.fixture(scope="session", autouse=True)
def driver_get():
    load_url(base_url)
    yield
    load_base_page(base_url)
    kill_driver_instance()


def slack_integration_flag(request):
    "pytest fixture for os version"
    return request.config.getoption("--slack")


# command line options
def pytest_addoption(parser):
    parser.addoption("--slack", "--slack_integration_flag",
                     dest="slack_integration_flag",
                     default="no",
                     help="Post the test report on slack channel: Y or N")
    parser.addoption("--build", action="store")


# pytest plugin hook
def pytest_sessionfinish(session, exitstatus):
    "executes after whole test run finishes."
    slack_value = 'no'
    for val in sys.argv:
        if '--slack' in val:
            slack_value = val.split('=')[1]
    if slack_value.lower() == 'yes':
        post_reports_to_slack()


def get_test_file_name():
    return os.getenv('PYTEST_CURRENT_TEST').split("::")[0].split("/")[-1].split(".py")[0]


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(3, html.th('Time', class_='sortable time', col='time'))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(getattr(report, 'description', '')))
    cells.insert(3, html.td(datetime.utcnow(), class_='col-time'))


def pytest_assertion_pass(expl):
    filter_data = re.split('== | in | > | >= | < | <= | !=', expl)
    logger.info(expl)
    if "True" in expl:
        logger.info(
            "Test Data for Pass Assertion ->" + " Actual: True" + " Expected: True" + ' PASS')
        logger.info(
            "Test Data for Pass Assertion ->" + " Actual: " + filter_data[0] + " Expected: " + filter_data[0] + ' PASS')


def pytest_exception_interact(report):
    logging.error(f'Test exception:\n{report.longreprtext}')


def pytest_runtest_protocol(item, nextitem):
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == 'setup':
            if report.failed:
                logger.info("SETUP FAILED!!!")
        if report.when == 'call':
            if report.failed:
                logger.info(f"Execution Result:{item.name}::{report.outcome.upper()}")
            elif report.passed:
                global test_name
                test_name = item.name
                logger.info(f"Execution Result:{test_name}::{report.outcome.upper()}")
    return True


def tear_down():
    global t1
    global outcome
    global current_file
    if collect_video in ["all", "on_failure"]:
        t1.join()
        report = outcome.get_result()
        if collect_video == "on_failure" and (report.passed or report.skipped):
            logger.info("Removing the video file as test passed or skipped :" + str(current_file))
            if os.path.exists(current_file):
                os.remove(current_file)


def create_folder(folder, file_name=None):
    if file_name is None:
        file_name = get_test_file_name()
    if not os.path.exists(os.path.join(os.path.sep, folder, file_name)):
        os.makedirs(os.path.join(os.path.sep, folder, file_name))
    return file_name


@pytest.fixture(scope="function", autouse=True)
def execute_teardown(request):
    request.addfinalizer(tear_down)


@pytest.fixture(scope="function", autouse=True)
def on_start():
    global t_array
    global t1
    global current_file
    test_case_name = str(os.getenv('PYTEST_CURRENT_TEST').split("::")[1].split(" ")[0])
    if collect_video in ["all", "on_failure"]:
        if not os.path.exists(screenrecorder_folder):
            os.makedirs(screenrecorder_folder)
        folder_name = create_folder(screenrecorder_folder)
        filename = test_case_name + ".avi"
        video_file_path = os.path.join(os.path.sep, screenrecorder_folder, folder_name, filename)
        current_file = video_file_path
        try:
            logger.info("Collect_video mode is:" + collect_video)
            if collect_video in ["all", "on_failure"]:
                logger.info("Video recording starting for test " + test_case_name)
                t1 = threading.Thread(target=set_screencapture, args=(test_case_name, video_file_path))
                t1.start()
        except Exception as e:
            logger.info("Video recording failed with Exception:", e)


def pytest_collection_modifyitems(config, items):
    rootdir = pathlib.Path(config.rootdir)
    for item in items:
        rel_path = pathlib.Path(item.fspath).relative_to(rootdir)
        mark_name = next((part for part in rel_path.parts if part.endswith('_tests')), '').removesuffix('_tests')
        if mark_name:
            mark = getattr(pytest.mark, mark_name)
            item.add_marker(mark)


def pytest_configure(config):
    rootdir = pathlib.Path(config.rootdir)
    for dir_ in rootdir.rglob('*_tests'):
        mark_name = dir_.stem.removesuffix('_tests')
        config.addinivalue_line('markers', mark_name)