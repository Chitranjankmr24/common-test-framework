from bs4 import BeautifulSoup
from helpers.pbank_api_client import get_request
from helpers.pbank_driver_manager import logger

product_url = "https://www.parasoft.com/products/"


def get_products():
    resp = get_request(product_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    for product in soup.find_all("h3"):
        if "Parasoft" in product.get_text().strip():
            logger.info(product.get_text().strip())
    return resp
