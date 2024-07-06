import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    client = APIClient()
    return client
