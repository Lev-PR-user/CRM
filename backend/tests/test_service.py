from data import service_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_service_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Услуга успешно создана"

    s_id = response.json()["service"]["id"]

    get_res_id = client.get(
        "/pservices/service_search",
        params={"услуга_id": s_id},
        headers=headers
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == s_id


def test_get_service_by_name(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Услуга успешно создана"

    s_id = response.json()["service"]["id"]
    s_name = service_data["услуга"]

    get_res_name = client.get(
        "/pservices/service_search",
        params={"услуга": s_name},
        headers=headers
    )

    assert get_res_name.status_code == 200
    items = get_res_name.json() if isinstance(get_res_name.json(), list) else [get_res_name.json()]
    assert any(item["id"] == s_id for item in items)
    assert all(item["service"] == s_name for item in items)


def test_get_service_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    get_res = client.get("/pservices/service_search", headers=headers)

    assert get_res.status_code == 400


def test_get_service_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    get_res = client.get(
        "/pservices/service_search",
        params={"услуга_id": 999999},
        headers=headers
    )

    assert get_res.status_code == 400


def test_get_all_services(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    s_id = response.json()["service"]["id"]

    get_res = client.get("/pservices/services", headers=headers)

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == s_id for item in items)

def test_create_service_without_token(client):
    response = client.post(
        "/services/service_create",
        json=service_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_service(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Услуга успешно создана"
    assert response.json()["service"]["service"] == service_data["услуга"]


def test_create_duplicate_service(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_create_service_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_service(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    service_id = response.json()["service"]["id"]

    update_res = client.put(
        "/services/service_update",
        params={"услуга_id": service_id},
        json={
            "услуга": "test"
        },
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Услуга успешно обновлена"
    assert update_res.json()["service"] == {
        "id": service_id,
        "service": "test"
    }


def test_update_duplicate_service(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    first_id = response.json()["service"]["id"]

    response2 = client.post(
        "/services/service_create",
        json={
            "услуга": "test"
        },
        headers=headers
    )

    second_id = response2.json()["service"]["id"]

    update_res = client.put(
        "/services/service_update",
        params={"услуга_id": second_id},
        json={
            "услуга": service_data["услуга"]
        },
        headers=headers
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]


def test_update_service_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    service_id = response.json()["service"]["id"]

    update_res = client.put(
        "/services/service_update",
        params={"услуга_id": service_id},
        json={"услуга": "test"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_service_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        "/services/service_update",
        params={"услуга_id": 999999},
        json={"услуга": "test"},
        headers=headers
    )

    assert update_res.status_code in (400, 500)


def test_delete_service(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    service_id = response.json()["service"]["id"]

    delete_res = client.delete(
        "/services/service_delete",
        params={"услуга_id": service_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Услуга успешно удалена"


def test_delete_service_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/services/service_create",
        json=service_data,
        headers=headers
    )

    service_id = response.json()["service"]["id"]

    delete_res = client.delete(
        "/services/service_delete",
        params={"услуга_id": service_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"