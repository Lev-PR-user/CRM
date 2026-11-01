from data import se_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_status_equipment_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Статус успешно создан"

    s_id = response.json()["status"]["id"]

    get_res_id = client.get(
        "/status_equipments/status_equipment_search",
        params={"статус_уведомления_id": s_id},
        headers=headers
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == s_id


def test_get_status_equipment_by_name(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Статус успешно создан"

    s_id = response.json()["status"]["id"]
    s_name = se_data["статус"]

    get_res_name = client.get(
        "/status_equipments/status_equipment_search",
        params={"статус": s_name},
        headers=headers
    )

    assert get_res_name.status_code == 200
    items = get_res_name.json() if isinstance(get_res_name.json(), list) else [get_res_name.json()]
    assert any(item["id"] == s_id for item in items)
    assert all(item["status_equipment"] == s_name for item in items)


def test_get_status_equipment_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    get_res = client.get(
        "/status_equipments/status_equipment_search",
        headers=headers
    )

    assert get_res.status_code == 400


def test_get_status_equipment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    get_res = client.get(
        "/status_equipments/status_equipment_search",
        params={"статус_уведомления_id": 999999},
        headers=headers
    )

    assert get_res.status_code == 400


def test_get_all_status_equipments(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    s_id = response.json()["status"]["id"]

    get_res = client.get(
        "/status_equipments/status_equipments",
        headers=headers
    )

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == s_id for item in items)


def test_get_status_equipments_without_token(client):
    response = client.get("/status_equipments/status_equipments")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_status_equipment_without_token(client):
    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_status_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Статус успешно создан"
    assert response.json()["status"]["status_equipment"] == se_data["статус"]


def test_create_duplicate_status_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_create_status_equipment_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_status_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    status_equipment_id = response.json()["status"]["id"]

    update_res = client.put(
        "/status_equipments/status_equipment_update",
        params={"статус_оборудования_id": status_equipment_id},
        json={
            "статус": "в ремонте"
        },
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Статус успешно обновлен"
    assert update_res.json()["status"]["status_equipment"] == "в ремонте"


def test_duplicate_status_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )
    first_id = response.json()["status"]["id"]

    response2 = client.post(
        "/status_equipments/status_equipment_create",
        json={
            "статус": "в ремонте"
        },
        headers=headers
    )
    second_id = response2.json()["status"]["id"]

    update_res = client.put(
        "/status_equipments/status_equipment_update",
        params={"статус_оборудования_id": first_id},
        json={
            "статус": "в ремонте"
        },
        headers=headers
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]


def test_update_status_equipment_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    status_equipment_id = response.json()["status"]["id"]

    update_res = client.put(
        "/status_equipments/status_equipment_update",
        params={"статус_оборудования_id": status_equipment_id},
        json={"статус": "в ремонте"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_status_equipment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        "/status_equipments/status_equipment_update",
        params={"статус_оборудования_id": 999999},
        json={"статус": "в ремонте"},
        headers=headers
    )

    assert update_res.status_code in (400, 500)


def test_delete_status_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    status_equipment_id = response.json()["status"]["id"]

    delete_res = client.delete(
        "/status_equipments/status_equipment_delete",
        params={"статус_оборудования_id": status_equipment_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Статус удален"


def test_delete_status_equipment_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/status_equipments/status_equipment_create",
        json=se_data,
        headers=headers
    )

    status_equipment_id = response.json()["status"]["id"]

    delete_res = client.delete(
        "/status_equipments/status_equipment_delete",
        params={"статус_оборудования_id": status_equipment_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"