from data import operator_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_operator_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оператор успешно создан"

    o_id = response.json()["operator"]["id"]

    get_res_id = client.get(
        "/operators/operator_search",
        params={"оператор_id": o_id},
        headers=headers
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == o_id


def test_get_operator_by_location(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оператор успешно создан"

    o_id = response.json()["operator"]["id"]
    o_location = operator_data["локации"][0]

    get_res_loc = client.get(
        "/operators/operator_search",
        params={"локации": o_location},
        headers=headers
    )

    assert get_res_loc.status_code == 200
    items = get_res_loc.json() if isinstance(get_res_loc.json(), list) else [get_res_loc.json()]
    assert any(item["id"] == o_id for item in items)


def test_get_operator_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    get_res = client.get("/operators/operator_search", headers=headers)

    assert get_res.status_code == 400


def test_get_operator_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    get_res = client.get(
        "/operators/operator_search",
        params={"оператор_id": 999999},
        headers=headers
    )

    assert get_res.status_code == 400


def test_get_all_operators(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    o_id = response.json()["operator"]["id"]

    get_res = client.get("/operators/operators", headers=headers)

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == o_id for item in items)


def test_get_operators_without_token(client):
    response = client.get("/operators/operators")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_operators_without_token(client):
    response = client.post(
        "/operators/operator_create",
        json=operator_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_operators(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оператор успешно создан"
    assert response.json()["operator"]["locationn"] == operator_data["локации"]
    assert response.json()["operator"]["shedule"] == operator_data["график"]


def test_create_operators_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательны для заполнения" in response.json()["detail"]


def test_update_operators(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    operators_id = response.json()["operator"]["id"]

    update_res = client.put(
        "/operators/operator_update",
        params={"оператор_id": operators_id},
        json={
            "пользователь": 1,
            "локации": [
                "пушкинская д 56"
            ],
            "график": {
                "пн-пт": "9:00-11:00"
            }
        },
        headers=headers
    )

    assert update_res.status_code == 200, update_res.json()
    assert update_res.json()["message"] == "Оператор успешно обновлен"
    assert update_res.json()["operator"] == {
        "id": operators_id,
        "user": 1,
        "locationn": [
            "пушкинская д 56"
        ],
        "shedule": {
            "пн-пт": "9:00-11:00"
        }
    }


def test_update_operators_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    operators_id = response.json()["operator"]["id"]

    update_res = client.put(
        "/operators/operator_update",
        params={"оператор_id": operators_id},
        json={"пользователь": 1}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"

def test_delete_operators(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    operators_id = response.json()["operator"]["id"]

    delete_res = client.delete(
        "/operators/operator_delete",
        params={"оператор_id": operators_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Оператор удален"


def test_delete_operators_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/operators/operator_create",
        json=operator_data,
        headers=headers
    )

    operators_id = response.json()["operator"]["id"]

    delete_res = client.delete(
        "/operators/operator_delete",
        params={"оператор_id": operators_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"