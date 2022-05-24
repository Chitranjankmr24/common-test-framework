import glob
from junitparser import JUnitXml, TestSuite, TestCase
from collections import defaultdict
import requests
import os
import logging

from helpers.pbank_env import base_url, slack_webhook


def post_reports_to_slack():
    xml = get_xml_report()
    total_tests = int(xml.tests)
    failed_error_skipped = xml.failures + xml.skipped + xml.errors
    failed_tests = xml.failures
    passed_tests = xml.tests - failed_error_skipped
    if passed_tests > 0 or failed_tests > 0:
        pass_percent = round(float(passed_tests * 100 / total_tests), 2)
        payload = f"UI Automation Test results: \n"f"Environment URL: https://{base_url}\n "f"Total TestCases Executed: {total_tests}\n" f"Passed: {passed_tests}\n"f"Failed: {xml.failures}\n"f"Skipped: {xml.skipped + xml.errors}\n"f"Pass Percentage: {pass_percent}{'%'}\n\n"f"Feature-wise Summary:\n " + '\n'
    else:
        payload = f"UI Automation Test results: \n"f"Environment URL: https://{base_url}\n" f"All the test cases are " \
                  f"skipped please look into it "
    post_request(payload)


def post_request(payload):
    headers = {"Content-Type": "application/json"}
    slack_response = requests.post(url=slack_webhook, json={"text": payload}, headers=headers)
    if slack_response.text == 'ok':
        logging.info('\n Successfully posted UI test execution pytest report on slack channel')
    else:
        logging.info('\n Something went wrong. Unable to post ui test execution pytest report on slack channel. slack '
                     'Response:', slack_response)


def get_xml_report():
    test_report_file = os.getcwd() + '//junitresults.xml'
    xml = JUnitXml.fromfile(test_report_file)
    return xml
