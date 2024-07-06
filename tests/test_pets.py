import pytest
from json import JSONDecodeError
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

@pytest.fixture
def create_pet(api_client):
    pet_data = {
        "id": 1,
        "name": "Goat",
        "status": "available",
        "photoUrls": ["link.example.com/goat.png"],
        "category": {"id": 1, "name": "Dogs"},
        "tags": [{"id": 0, "name": "Cute"}]
    }
    response = api_client.post("/pet", json=pet_data)
    assert response.status_code == 200
    yield
    api_client.delete(f"/pet/{pet_data['id']}") 

@pytest.mark.parametrize("pet_id, expected_status, validate_function", [
    (1, 200, lambda data: data['name'] == 'Goat' and data['status'] == 'available'),
    (2, 200, lambda data: data['name'] == 'UpdatedBird' and data['status'] == 'sold')
])
def test_get_pet(api_client, create_pet, pet_id, expected_status, validate_function):
    response = api_client.get(f"/pet/{pet_id}")
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
    if expected_status == 200:
        data = response.json()
        assert validate_function(data), f"Data validation failed for pet ID {pet_id}, data: {data}"

@pytest.mark.parametrize("pet_data, expected_name", [
    ({"id": 1, "category": {"id": 1, "name": "dogs"}, "name": "TestDog", "photoUrls": ["https://unsplash.com/photos/black-pug-with-gray-knit-scarf-Mv9hjnEUHR4"], "tags": [{"id": 1, "name": "tag1"}], "status": "available"}, "TestDog"),
    ({"id": 2, "category": {"id": 2, "name": "cats"}, "name": "TestCat", "photoUrls": ["https://unsplash.com/photos/white-and-brown-long-fur-cat-ZCHj_2lJP00"], "tags": [{"id": 2, "name": "tag2"}], "status": "available"}, "TestCat")
])
def test_add_pet(api_client, pet_data, expected_name):
    response = api_client.post("/pet", json=pet_data)
    assert response.status_code == 200
    assert response.json()['name'] == expected_name, f"Expected name '{expected_name}' but got '{response.json()['name']}'"

@pytest.mark.parametrize("updated_data, expected_name", [
    ({"id": 1, "category": {"id": 1, "name": "cats"}, "name": "UpdatedCat", "photoUrls": ["https://unsplash.com/photos/white-and-brown-long-fur-cat-ZCHj_2lJP00"], "tags": [{"id": 1, "name": "tag2"}], "status": "sold"}, "UpdatedCat"),
    ({"id": 2, "category": {"id": 2, "name": "birds"}, "name": "UpdatedBird", "photoUrls": ["https://example.com/photo"], "tags": [{"id": 2, "name": "tag3"}], "status": "sold"}, "UpdatedBird")
])
def test_update_pet(api_client, updated_data, expected_name):
    response = api_client.put("/pet", json=updated_data)
    assert response.status_code == 200
    assert response.json()['name'] == expected_name, f"Expected name '{expected_name}' but got '{response.json()['name']}'"

@pytest.mark.parametrize("pet_id, expected_status", [
    (1, 200),
    (99999, 404)
])
def test_delete_pet(api_client, pet_id, expected_status):
    response = api_client.delete(f"/pet/{pet_id}")
    assert response.status_code == expected_status
    try:
        response_data = response.json()
        print(response_data)
    except JSONDecodeError:
        print("No JSON data in response")