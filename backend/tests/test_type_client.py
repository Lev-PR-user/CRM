from .data import type_client_data

def test_create_type_client(client):
    response = client.post(
        "/type_client/type_client_create",
        json = type_client_data
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Тип клиента успешно добавлен"
    assert response.json()["type_client"]["type"] == "ИП"

def test_create_duplicate_type_client(client):

    client.post(
        "/type_client/type_client_create",
        json = type_client_data
    )

    response = client.post(
        "/type_client/type_client_create",
        json = type_client_data
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_create_type_client_empty(client):
    response = client.post(
        "/type_client/type_client_create",
        json = {}
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]

def test_update_type_client(client):

    client.post(
        "/type_client/type_client_create",
        json = type_client_data
    )

    type_client_id = 1

    update_res = client.put(
        f"/type_client/type_client_update?тип_клиента_id={type_client_id}",
        json = {
            "тип": "Физ. лицо"
        }
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Тип клиента обновлен"
    assert update_res.json()["type_client"]["type"] == "Физ. лицо"

def test_duplicate_update_type_client(client):

    client.post(
        "/type_client/type_client_create",
        json = type_client_data
    )

    client.post(
        "/type_client/type_client_create",
        json = {
            "тип": "Физ. лицо"
        }
    )

    type_client_name = "ИП"

    update_res = client.put(
        f"/type_client/type_client_update?тип={type_client_name}",
        json = {
            "тип": "Физ. лицо"
        }
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]

def test_delete_type_client(client):

    client.post(
        "/type_client/type_client_create",
        json = type_client_data
    )

    type_client_id = 1

    delete_res = client.delete(f"/type_client/type_client_delete?тип_клиента_id={type_client_id}")

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Тип успешно удален"