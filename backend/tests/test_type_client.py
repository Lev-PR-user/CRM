from data import type_client_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_type_client_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Тип клиента успешно добавлен"

    tc_id = response.json()["type_client"]["id"]

    get_res_id = client.get(
        "/type_clients/type_client_search",
        params={"тип_клиента_id": tc_id},
        headers=headers
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == tc_id


def test_get_type_client_by_name(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Тип клиента успешно добавлен"

    tc_id = response.json()["type_client"]["id"]
    tc_type = type_client_data["тип"]

    get_res_name = client.get(
        "/type_clients/type_client_search",
        params={"тип": tc_type},
        headers=headers
    )

    assert get_res_name.status_code == 200
    items = get_res_name.json() if isinstance(get_res_name.json(), list) else [get_res_name.json()]
    assert any(item["id"] == tc_id for item in items)
    assert all(item["type"] == tc_type for item in items)


def test_get_type_client_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    get_res = client.get("/type_clients/type_client_search", headers=headers)

    assert get_res.status_code == 400


def test_get_type_client_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    get_res = client.get(
        "/type_clients/type_client_search",
        params={"тип_клиента_id": 999999},
        headers=headers
    )

    assert get_res.status_code == 400


def test_get_all_type_clients(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    tc_id = response.json()["type_client"]["id"]

    get_res = client.get("/type_clients/type_clients", headers=headers)

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == tc_id for item in items)


def test_get_type_clients_without_token(client):
    response = client.get("/type_clients/type_clients")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_type_client_without_token(client):
    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_type_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Тип клиента успешно добавлен"
    assert response.json()["type_client"]["type"] == type_client_data["тип"]


def test_create_duplicate_type_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_create_type_client_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_type_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    type_client_id = response.json()["type_client"]["id"]

    update_res = client.put(
        "/type_clients/type_client_update",
        params={"тип_клиента_id": type_client_id},
        json={
            "тип": "Физ. лицо"
        },
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Тип клиента обновлен"
    assert update_res.json()["type_client"]["type"] == "Физ. лицо"


def test_duplicate_update_type_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )
    first_id = response.json()["type_client"]["id"]

    response2 = client.post(
        "/type_clients/type_client_create",
        json={
            "тип": "Физ. лицо"
        },
        headers=headers
    )
    second_id = response2.json()["type_client"]["id"]

    update_res = client.put(
        "/type_clients/type_client_update",
        params={"тип_клиента_id": first_id},
        json={
            "тип": "Физ. лицо"
        },
        headers=headers
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]


def test_update_type_client_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    type_client_id = response.json()["type_client"]["id"]

    update_res = client.put(
        "/type_clients/type_client_update",
        params={"тип_клиента_id": type_client_id},
        json={"тип": "Физ. лицо"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_type_client_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        "/type_clients/type_client_update",
        params={"тип_клиента_id": 999999},
        json={"тип": "Физ. лицо"},
        headers=headers
    )

    assert update_res.status_code in (400, 500)


def test_delete_type_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    type_client_id = response.json()["type_client"]["id"]

    delete_res = client.delete(
        "/type_clients/type_client_delete",
        params={"тип_клиента_id": type_client_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Тип успешно удален"


def test_delete_type_client_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/type_clients/type_client_create",
        json=type_client_data,
        headers=headers
    )

    type_client_id = response.json()["type_client"]["id"]

    delete_res = client.delete(
        "/type_clients/type_client_delete",
        params={"тип_клиента_id": type_client_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"