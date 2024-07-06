import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

@pytest.mark.parametrize("order_data, expected_status", [
    ({"id": 10, "petId": -1, "quantity": -1, "shipDate": "not-a-date", "status": "invalid-status", "complete": "yes"}, 400),
    ({}, 400),
    ({"id": "abc", "petId": "xyz", "quantity": "one", "shipDate": "2023-07-07T14:00:00.000Z", "status": "placed", "complete": True}, 400)
])
def test_add_invalid_order(api_client, order_data, expected_status):
    response = api_client.post("/store/order", json=order_data)
    print(f"Order Data: {order_data}")
    print(f"Response Status Code: {response.status_code}")
    try:
        print(f"Response Body: {response.json()}")
    except Exception as e:
        print(f"Could not decode JSON response: {e}")
    
    # Логирование дополнительной информации
    if response.status_code != expected_status:
        print(f"Unexpected response code: {response.status_code}, expected: {expected_status}")
        print(f"Response text: {response.text}")
    
    assert response.status_code == expected_status, f"Expected HTTP {expected_status} for invalid order data, got {response.status_code}"

@pytest.mark.parametrize("order_id, expected_status", [
    (1, 200),
    (99999, 404)
])
def test_get_order(api_client, order_id, expected_status):
    response = api_client.get(f"/store/order/{order_id}")
    assert response.status_code == expected_status, f"Expected status code {expected_status}, got {response.status_code}"

@pytest.mark.parametrize("order_data, expected_status", [
    ({"id": 10, "petId": 1, "quantity": 1, "shipDate": "2023-07-07T14:00:00.000Z", "status": "placed", "complete": True}, 200),
    ({"id": 11, "petId": 2, "quantity": 2, "shipDate": "2023-07-07T14:00:00.000Z", "status": "placed", "complete": False}, 200)
])
def test_add_order(api_client, order_data, expected_status):
    response = api_client.post("/store/order", json=order_data)
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json()['id'] == order_data['id'], f"Expected order ID {order_data['id']}"

@pytest.mark.parametrize("order_id, expected_status", [
    (10, 200),
    (11, 200),
    (99999, 404)
])
def test_delete_order(api_client, order_id, expected_status):
    response = api_client.delete(f"/store/order/{order_id}")
    assert response.status_code == expected_status
    if expected_status == 200:
        check_response = api_client.get(f"/store/order/{order_id}")
        assert check_response.status_code == 404, "Order should be deleted but still exists"
