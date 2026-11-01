from data import user_data, user_login_email, user_login_number, user_data_answer

def _create_role(client, name="user", description="Обычный пользователь"):
    res = client.post("/roles/createrole", json={"название_роли": name, "описание": description})
    assert res.status_code == 200, res.json()
    return res.json()["role"]["id"]

def _register_and_login(client, register_data, login_data):
    reg = client.post("/pusers/registers", json=register_data)
    assert reg.status_code == 200, reg.json()

    login = client.post("/pusers/login", json=login_data)
    assert login.status_code == 200, login.json()

    token = login.json()["token"]
    user = login.json()["user"]
    return user, {"Authorization": f"Bearer {token}"}

def test_register_user(client):
    response = client.post(
        "/pusers/registers",
        json=user_data
    )
    assert response.status_code == 200, response.json()
    assert response.json()["message"] == "Пользователь создан"
    assert response.json()["user"]["email"] == "ivan@example.com"
    assert "token" in response.json()

def test_register_duplicate_email(client):
    first = client.post("/pusers/registers", json=user_data)
    assert first.status_code == 200, first.json()

    response = client.post("/pusers/registers", json=user_data)
    assert response.status_code == 400, response.json()
    assert "уже существует" in response.json()["detail"]


def test_login_user(client):
    reg = client.post(
        "/pusers/registers",
        json=user_data
    )
    assert reg.status_code == 200, reg.json()

    response = client.post(
        "/pusers/login",
        json=user_login_email,
    )
    assert response.status_code == 200, response.json()
    assert "token" in response.json()

    response2 = client.post(
        "/pusers/login",
        json=user_login_number,
    )
    assert response2.status_code == 200, response2.json()
    assert "token" in response2.json()


def test_login_wrong_password(client):
    reg = client.post(
        "/pusers/registers",
        json=user_data
    )
    assert reg.status_code == 200, reg.json()

    response = client.post(
        "/pusers/login",
        json={"почта": "ivan@example.com", "пароль": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный логин или пароль"

def test_update_user(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        f"/users/update",
        json={
            "имя": "НовоеИмя",
            "номер": "79997777777",
            },
         headers=headers
    )
    assert update_res.status_code == 200, update_res.json()
    assert update_res.json()["user"]["name"] == "НовоеИмя"
    assert update_res.json()["user"]["number"] == "79997777777"

def test_profile(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    profile_res = client.get(
        f"/users/profile",
        headers=headers
    )

    assert profile_res.status_code == 200
    assert profile_res.json()["user"] == user_data_answer

def test_profile_without_token(client):

    profile_res = client.get(
        f"/users/profile"
    )

    assert profile_res.status_code == 401
    assert profile_res.json()["detail"] == "Not authenticated"

def test_delete_user(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    delete_res = client.delete(
        f"/users/delete",
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Пользователь удален"
