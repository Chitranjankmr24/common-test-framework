from helpers.pbank_api_client import post_call
from helpers.pbank_env import api_base_url

delete_db_resource = "cleanDB"


def clean_db_request():
    post_call(f"{api_base_url}{delete_db_resource}")
