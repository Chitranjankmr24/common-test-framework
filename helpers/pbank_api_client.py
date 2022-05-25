import requests
from urllib3 import Retry
from helpers.pbank_driver_manager import logger

session = requests.Session()
retries = Retry(total=5, connect=10, backoff_factor=1,
                status_forcelist=[500, 502, 503, 504])
adapter = requests.adapters.HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)


def create_headers(username=None, apikey=None, bearer_token=None):
    if username and apikey:
        headers = {
            'username': username,
            'apikey': apikey,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    elif username and bearer_token:
        headers = {
            'username': username,
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    return headers


def get_request(host_url, username=None, apikey=None, bearer_token=None, raise_exception=True):
    headers = create_headers(username, apikey, bearer_token)
    json_resp = session.get(url=host_url, headers=headers)
    logger.info("json_resp.status_code " + str(json_resp.status_code))

    return json_resp


def post_request(host_url, json_payload=None, username=None, apikey=None, bearer_token=None):
    headers = create_headers(username, apikey, bearer_token)
    json_resp = session.post(url=host_url, data=json_payload, headers=headers)
    logger.info("json_resp.status_code " + str(json_resp.status_code))
    return json_resp


def put_request(host_url, json_payload=None, username=None, apikey=None, bearer_token=None):
    headers = create_headers(username, apikey, bearer_token)
    json_resp = session.put(url=host_url, data=json_payload, headers=headers)
    logger.info("json_resp.status_code " + str(json_resp.status_code))
    return json_resp


def delete_request(host_url, username=None, apikey=None, bearer_token=None):
    headers = create_headers(username, apikey, bearer_token)
    json_resp = session.delete(url=host_url, headers=headers)
    logger.info("json_resp.status_code " + str(json_resp.status_code))
    return json_resp
