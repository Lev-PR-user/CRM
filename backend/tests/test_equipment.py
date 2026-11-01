from data import equipment_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_equipment_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"

    e_id = response.json()["eqiupment"]["id"]

    get_res_id = client.get(
        "/pequipments/equipment_search",
        params={"оборудование_id": e_id}
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == e_id


def test_get_equipment_by_model(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"

    e_id = response.json()["eqiupment"]["id"]
    e_model = equipment_data["модель"]

    get_res_model = client.get(
        "/pequipments/equipment_search",
        params={"модель": e_model}
    )

    assert get_res_model.status_code == 200
    items = get_res_model.json() if isinstance(get_res_model.json(), list) else [get_res_model.json()]
    assert any(item["id"] == e_id for item in items)
    assert all(item["model"] == e_model for item in items)


def test_get_equipment_by_series(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"

    e_id = response.json()["eqiupment"]["id"]
    e_series = equipment_data["серия"]

    get_res_series = client.get(
        "/pequipments/equipment_search",
        params={"серия": e_series}
    )

    assert get_res_series.status_code == 200
    items = get_res_series.json() if isinstance(get_res_series.json(), list) else [get_res_series.json()]
    assert any(item["id"] == e_id for item in items)
    assert all(item["series"] == e_series for item in items)


def test_get_equipment_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    get_res = client.get("/pequipments/equipment_search")

    assert get_res.status_code == 400


def test_get_equipment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    get_res = client.get(
        "/pequipments/equipment_search",
        params={"оборудование_id": 999999}
    )

    assert get_res.status_code == 400


def test_get_all_equipments(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    e_id = response.json()["eqiupment"]["id"]

    get_res = client.get("/pequipments/equipments")

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == e_id for item in items)


def test_create_equipment_without_token(client):
    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"
    assert response.json()["eqiupment"]["model"] == equipment_data["модель"]
    assert response.json()["eqiupment"]["series"] == equipment_data["серия"]
    assert response.json()["eqiupment"]["status"] == equipment_data["статус"]
    assert response.json()["eqiupment"]["location"] == equipment_data["расположение"]
    
def test_create_equipment_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["eqiupment"]["id"]

    update_res = client.put(
        "/equipments/update_equipment",
        params={"оборудование_id": equipment_id},
        json={
            "модель": "Sdt",
            "серия": "345wd",
            "статус": 3,
            "расположение": 2
        },
        headers=headers
    )

    assert update_res.status_code == 200, f"status={update_res.status_code}, body={update_res.text}"
    assert update_res.json()["message"] == "оборудование обновлено"
    assert update_res.json()["eqiupment"] == {
        "id": equipment_id,
        "model": "Sdt",
        "series": "345wd",
        "status": 3,
        "location": 2
    }


def test_update_equipment_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["eqiupment"]["id"]

    update_res = client.put(
        "/equipments/update_equipment",
        params={"оборудование_id": equipment_id},
        json={"модель": "x"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_equipment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        "/equipments/update_equipment",
        params={"оборудование_id": 999999},
        json={"модель": "x"},
        headers=headers
    )

    assert update_res.status_code == 500


def test_delete_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["eqiupment"]["id"]

    delete_res = client.delete(
        "/equipments/delete_equipment",
        params={"оборудование_id": equipment_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Оборудование удалено"


def test_delete_equipment_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/equipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["eqiupment"]["id"]

    delete_res = client.delete(
        "/equipments/delete_equipment",
        params={"оборудование_id": equipment_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"