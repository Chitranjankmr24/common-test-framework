from helpers.pbank_api_client import post_request
from helpers.pbank_env import api_base_url

delete_db_resource = "cleanDB"


def clean_db_request():
    res = post_request(f"{api_base_url}{delete_db_resource}")
    return res
