from data import client_data, user_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_client_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Клиент создан"

    c_id = response.json()["client"]["id"]

    get_res_id = client.get(
        "/pclients/client_search",
        params={"клиент_id": c_id}
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == c_id

def test_get_client_by_name(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Клиент создан"

    c_id = response.json()["client"]["id"]
    c_name = client_data["имя"]

    get_res_name = client.get(
        "/pclients/client_search",
        params={"имя": c_name}
    )

    assert get_res_name.status_code == 200
    items = get_res_name.json() if isinstance(get_res_name.json(), list) else [get_res_name.json()]
    assert any(item["id"] == c_id for item in items)
    assert all(item["name"] == c_name for item in items)


def test_get_client_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    get_res = client.get("/pclients/client_search")

    assert get_res.status_code == 400

def test_get_client_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    get_res = client.get(
        "/pclients/client_search",
        params={"клиент_id": 999999}
    )

    assert get_res.status_code == 400

def test_get_all_clients(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    c_id = response.json()["client"]["id"]

    get_res = client.get("/pclients/clients")

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == c_id for item in items)


def test_create_client_without_token(client):
    response = client.post(
        "/clients/client_create",
        json=client_data,
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_create_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Клиент создан"
    assert response.json()["client"]["name"] == client_data["имя"]
    assert response.json()["client"]["type"] == client_data["тип"]
    assert response.json()["client"]["notes"] == client_data["заметки"]
    assert response.json()["client"]["contacts"] == client_data["контакты"]

def test_create_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    client_id = response.json()["client"]["id"]

    update_res = client.patch(
        "/clients/client_update",
        params={"клиент_id": client_id},
        json={
            "имя": "тест",
            "тип": 5,
            "заметки": "",
            "контакты": {
                "номер": "87777777777",
                "почта": "test_mail.yandex.ru"
            }
        },
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Клиент успешно обновлен"
    assert update_res.json()["client"] == {
        "id": client_id,
        "name": "тест",
        "type": 5,
        "notes": "",
        "contacts": {
            "номер": "87777777777",
            "почта": "test_mail.yandex.ru"
        }
    }


def test_update_client_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    client_id = response.json()["client"]["id"]

    update_res = client.patch(
        "/clients/client_update",
        params={"клиент_id": client_id},
        json={"имя": "x"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_client_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.patch(
        "/clients/client_update",
        params={"клиент_id": 999999},
        json={"имя": "x"},
        headers=headers
    )

    assert update_res.status_code == 500


def test_delete_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    client_id = response.json()["client"]["id"]

    delete_res = client.delete(
        "/clients/client_delete",
        params={"клиент_id": client_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Клиент удален"


def test_delete_client_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/clients/client_create",
        json=client_data,
        headers=headers
    )

    client_id = response.json()["client"]["id"]

    delete_res = client.delete(
        "/clients/client_delete",
        params={"клиент_id": client_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"