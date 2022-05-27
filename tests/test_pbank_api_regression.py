import pytest
from pages.clean_db_page import clean_db_request
from pages.product_page import get_products

pytestmark = pytest.mark.api

def test_verify_products():
    """Verify products"""
    res = get_products()
    assert res.status_code == 200


@pytest.mark.order('last')
def test_db_clean_api():
    """Clean DB API"""
    res = clean_db_request()
    assert res.status_code == 204

