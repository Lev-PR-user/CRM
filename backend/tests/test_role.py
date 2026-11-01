from data import role_data_admin, role_data_user, role_data
from data_def import _register_and_login
from data import user_data, user_login_number

def test_get_role_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_admin,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["Message"] == "роль создана успешно"

    r_id = response.json()["role"]["id"]

    get_res_id = client.get(
        "/roles/role_search",
        params={"роль_id": r_id},
        headers=headers
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == r_id


def test_get_role_by_name(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_admin,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["Message"] == "роль создана успешно"

    r_id = response.json()["role"]["id"]
    r_name = role_data_admin["название_роли"]

    get_res_name = client.get(
        "/roles/role_search",
        params={"название_роли": r_name},
        headers=headers
    )

    assert get_res_name.status_code == 200
    items = get_res_name.json() if isinstance(get_res_name.json(), list) else [get_res_name.json()]
    assert any(item["id"] == r_id for item in items)
    assert all(item["name"] == r_name for item in items)


def test_get_role_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/roles/createrole",
        json=role_data_admin,
        headers=headers
    )

    get_res = client.get("/roles/role_search", headers=headers)

    assert get_res.status_code == 400


def test_get_role_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/roles/createrole",
        json=role_data_admin,
        headers=headers
    )

    get_res = client.get(
        "/roles/role_search",
        params={"роль_id": 999999},
        headers=headers
    )

    assert get_res.status_code == 400


def test_get_all_roles(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_admin,
        headers=headers
    )

    r_id = response.json()["role"]["id"]

    get_res = client.get("/roles/roles", headers=headers)

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == r_id for item in items)


def test_get_roles_without_token(client):
    response = client.get("/roles/roles")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_role_without_token(client):
    response = client.post(
        "/roles/createrole",
        json=role_data_user
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_role(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_admin,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["Message"] == "роль создана успешно"
    assert response.json()["role"]["name"] == role_data_admin["название_роли"]
    assert response.json()["role"]["description"] == role_data_admin["описание"]


def test_create_duplicate_role(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post("/roles/createrole", json=role_data, headers=headers)

    response = client.post("/roles/createrole", json=role_data, headers=headers)

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


def test_create_role_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_role(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_user,
        headers=headers
    )

    role_id = response.json()["role"]["id"]

    update_res = client.put(
        "/roles/update",
        params={"роль_id": role_id},
        json={"название_роли": "superuser", "описание": "Обновленное описание"},
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Роль успешно обновлена"
    assert update_res.json()["role"]["name"] == "superuser"


def test_update_role_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_user,
        headers=headers
    )

    role_id = response.json()["role"]["id"]

    update_res = client.put(
        "/roles/update",
        params={"роль_id": role_id},
        json={"название_роли": "superuser"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_role_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        "/roles/update",
        params={"роль_id": 999999},
        json={"название_роли": "superuser"},
        headers=headers
    )

    assert update_res.status_code in (400, 500)


def test_delete_role(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_user,
        headers=headers
    )

    role_id = response.json()["role"]["id"]

    delete_res = client.delete(
        "/roles/delete",
        params={"роль_id": role_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Роль успешно удалена"


def test_delete_role_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/roles/createrole",
        json=role_data_user,
        headers=headers
    )

    role_id = response.json()["role"]["id"]

    delete_res = client.delete(
        "/roles/delete",
        params={"роль_id": role_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"