from data import location_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_location_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Локация успешно добавлена"

    l_id = response.json()["location"]["id"]

    get_res_id = client.get(
        "/plocations/location_search",
        params={"локация_id": l_id}
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == l_id

def test_get_location_by_name(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Локация успешно добавлена"

    l_id = response.json()["location"]["id"]
    l_name = location_data["название"]

    get_res_name = client.get(
        "/plocations/location_search",
        params={"название": l_name}
    )

    assert get_res_name.status_code == 200
    items = get_res_name.json() if isinstance(get_res_name.json(), list) else [get_res_name.json()]
    assert any(item["id"] == l_id for item in items)
    assert all(item["name"] == l_name for item in items)


def test_get_location_by_address(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Локация успешно добавлена"

    l_id = response.json()["location"]["id"]
    l_address = location_data["адрес"]

    get_res_address = client.get(
        "/plocations/location_search",
        params={"адрес": l_address}
    )

    assert get_res_address.status_code == 200
    items = get_res_address.json() if isinstance(get_res_address.json(), list) else [get_res_address.json()]
    assert any(item["id"] == l_id for item in items)
    assert all(item["address"] == l_address for item in items)


def test_get_location_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    get_res = client.get("/plocations/location_search")

    assert get_res.status_code == 400


def test_get_location_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    get_res = client.get(
        "/plocations/location_search",
        params={"локация_id": 999999}
    )

    assert get_res.status_code == 400


def test_get_all_locations(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    l_id = response.json()["location"]["id"]

    get_res = client.get("/plocations/locations")

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == l_id for item in items)


def test_create_location_without_token(client):
    response = client.post(
        "/locations/location_create",
        json=location_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_location(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Локация успешно добавлена"
    assert response.json()["location"]["name"] == location_data["название"]
    assert response.json()["location"]["address"] == location_data["адрес"]
    assert response.json()["location"]["openning_hours"] == location_data["часы_работы"]

def test_create_duplicate_location(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]

def test_create_location_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_location(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    location_id = response.json()["location"]["id"]

    update_res = client.put(
        "/locations/location_update",
        params={"локация_id": location_id},
        json={
            "название": "тексел",
            "адрес": "пушкинская д 6",
            "часы_работы": {
                "пн-пт": "09:00-18:00",
                "сб": "10:00-15:00",
                "вс": "выходной"
            }
        },
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Локация успешно обновлена"
    assert update_res.json()["location"] == {
        "id": location_id,
        "name": "тексел",
        "address": "пушкинская д 6",
        "openning_hours": {
            "пн-пт": "09:00-18:00",
            "сб": "10:00-15:00",
            "вс": "выходной"
        }
    }

def test_update_duplicate_location(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    client.post(
        "/locations/location_create",
        json={
            "название": "тексел",
            "адрес": "тестовая д 6",
            "часы_работы": {
                "пн-пт": "09:00-21:00",
                "сб": "10:00-14:00",
                "вс": "выходной"
            }
        },
        headers=headers
    )

    location_id = 1

    update_res = client.put(
        "/locations/location_update",
        params={"локация_id": location_id},
        json={
            "название": "тексел",
            "адрес": "тестовая д 6",
            "часы_работы": {
                "пн-пт": "09:00-21:00",
                "сб": "10:00-14:00",
                "вс": "выходной"
            }
        },
        headers=headers
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]

def test_update_location_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    location_id = response.json()["location"]["id"]

    update_res = client.put(
        "/locations/location_update",
        params={"локация_id": location_id},
        json={"название": "x"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_location_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        "/locations/location_update",
        params={"локация_id": 999999},
        json={"название": "x"},
        headers=headers
    )

    assert update_res.status_code == 500


def test_delete_location(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    location_id = response.json()["location"]["id"]

    delete_res = client.delete(
        "/locations/location_delete",
        params={"локация_id": location_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "локация удалена"


def test_delete_location_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/locations/location_create",
        json=location_data,
        headers=headers
    )

    location_id = response.json()["location"]["id"]

    delete_res = client.delete(
        "/locations/location_delete",
        params={"локация_id": location_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"