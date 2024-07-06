import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

@pytest.fixture
def create_user(api_client):
    user_data = {
        "id": 1,
        "username": "testuser",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 0
    }
    response = api_client.post("/user", json=user_data)
    assert response.status_code == 200
    yield
    api_client.delete(f"/user/{user_data['username']}")

@pytest.mark.parametrize("username, expected_status, validate_function", [
    ("testuser", 200, lambda data: data['username'] == 'testuser' and data['email'] == 'testuser@example.com'),
    ("nonexistentuser", 404, None)
])
def test_get_user(api_client, create_user, username, expected_status, validate_function):
    response = api_client.get(f"/user/{username}")
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
    if expected_status == 200:
        data = response.json()
        assert validate_function(data), f"Data validation failed for username {username}, data: {data}"

@pytest.mark.parametrize("user_data, expected_username", [
    ({"id": 2, "username": "newuser", "firstName": "New", "lastName": "User", "email": "newuser@example.com", "password": "password123", "phone": "0987654321", "userStatus": 1}, "newuser"),
])
def test_add_user(api_client, user_data, expected_username):
    response = api_client.post("/user", json=user_data)
    assert response.status_code == 200

    # Проверка, что пользователь действительно создан
    response = api_client.get(f"/user/{expected_username}")
    assert response.status_code == 200, f"Expected HTTP 200 for getting the user, got {response.status_code}"
    assert response.json()['username'] == expected_username, f"Expected username '{expected_username}' but got '{response.json()['username']}'"

@pytest.mark.parametrize("updated_data, expected_username", [
    ({"id": 1, "username": "testuser", "firstName": "Updated", "lastName": "User", "email": "updateduser@example.com", "password": "newpassword123", "phone": "1112223333", "userStatus": 1}, "testuser"),
])
def test_update_user(api_client, create_user, updated_data, expected_username):
    response = api_client.put(f"/user/{expected_username}", json=updated_data)
    assert response.status_code == 200

    # Проверка, что данные пользователя действительно обновлены
    response = api_client.get(f"/user/{expected_username}")
    assert response.status_code == 200
    assert response.json()['username'] == expected_username, f"Expected username '{expected_username}' but got '{response.json()['username']}'"
    assert response.json()['firstName'] == updated_data['firstName'], f"Expected first name '{updated_data['firstName']}' but got '{response.json()['firstName']}'"

@pytest.mark.parametrize("username, expected_status", [
    ("testuser", 200),
    ("nonexistentuser", 404)
])
def test_delete_user(api_client, create_user, username, expected_status):
    response = api_client.delete(f"/user/{username}")
    assert response.status_code == expected_status
    if expected_status == 200:
        check_response = api_client.get(f"/user/{username}")
        assert check_response.status_code == 404, f"User {username} should be deleted but still exists"
