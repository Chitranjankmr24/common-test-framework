import glob
from junitparser import JUnitXml, TestSuite, TestCase
from collections import defaultdict
import requests
import os
import logging

from helpers.pbank_env import base_url, slack_webhook

class_set = set()


def post_reports_to_slack():
    global class_set
    result_dict = defaultdict(list)
    xml = get_xml_report()
    if xml.tests > 0:
        for suite in xml:
            for case in suite:
                if case.classname and "tests" in case.classname:
                    class_set.add(case.classname)
                    result_dict[get_feature_name(case.classname)].append(translate_result(case.result))
        create_payload(generate_result(result_dict), xml)


def translate_result(result):
    result_list = ['failure', 'skipped', 'error']
    if len(result) > 0:
        test = str(result).split(' ')[1].replace("'", "")
        if test in result_list:
            return "SKIPPED" if test in 'error' else test.upper()
    else:
        return "PASSED"


def generate_result(result):
    payload_data = ""
    for key, values in result.items():
        res_dict = {}
        for value in values:
            if res_dict.get(value):
                res_dict[value] = res_dict.get(value) + 1
            else:
                res_dict[value] = 1
        final_data = key.replace("_", " ").title() + " - " + "Passed: " + integer(
            res_dict.get('PASSED')) + " " + "Failed: " + integer(
            res_dict.get('FAILURE')) + " " + "Skipped: " + integer(res_dict.get('SKIPPED'))
        payload_data += final_data + '\n'
    return payload_data


def get_feature_name(class_name):
    feature_name = class_name.split("_")
    del feature_name[0:2]
    return "_".join(feature_name)


def integer(value):
    return str(0) if value is None else str(value)


def create_payload(final_payload, xml):
    total_tests = int(xml.tests)
    failed_error_skipped = xml.failures + xml.skipped + xml.errors
    failed_tests = xml.failures
    passed_tests = xml.tests - failed_error_skipped
    if passed_tests > 0 or failed_tests > 0:
        pass_percent = round(float(passed_tests * 100 / total_tests), 2)
        payload = f"Para Bank Automation Test results: \n\n"f"Environment URL: {base_url}\n" f"Total TestCases Executed: {total_tests}\n" f"Passed: {passed_tests}\n"f"Failed: {xml.failures}\n"f"Skipped: {xml.skipped + xml.errors}\n"f"Pass Percentage: {pass_percent}{'%'}\n\n"f"Feature-wise Summary:\n " + '\n'
        payload += final_payload
    else:
        payload = f"Para Bank Automation Test results: \n\n"f"Environment URL: {base_url}\n"f"All the test cases are skipped please look into it"
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

