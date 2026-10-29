def _create_role(client, name="user", description="Обычный пользователь"):
    res = client.post("/roles/createrole", json={"название_роли": name, "описание": description})
    assert res.status_code == 200, res.json()
    return res.json()["role"]["id"]


def test_register_user(client):
    role_id = _create_role(client, "admin", "Админ")

    response = client.post(
        "/users/registers",
        json={
            "фамилия": "Иванов",
            "имя": "Иван",
            "пароль": "securepassword",
            "отчество": "Иванович",
            "название_организации": "ООО Ромашка",
            "почта": "ivan@example.com",
            "номер": "79991234567",
            "роль": 1,
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json()["message"] == "Пользователь создан"
    assert response.json()["user"]["email"] == "ivan@example.com"
    assert "token" in response.json()


def test_register_duplicate_email(client):
    role_id = _create_role(client)

    user_data = {
        "фамилия": "Петров",
        "имя": "Петр",
        "пароль": "password123",
        "почта": "petrov@example.com",
        "номер": "79990000000",
        "роль": role_id,
    }

    first = client.post("/users/registers", json=user_data)
    assert first.status_code == 200, first.json()

    response = client.post("/users/registers", json=user_data)
    assert response.status_code == 400, response.json()
    assert "уже существует" in response.json()["detail"]


def test_login_user(client):
    role_id = _create_role(client)

    reg = client.post(
        "/users/registers",
        json={
            "фамилия": "Сидоров",
            "имя": "Сидор",
            "пароль": "mypassword",
            "почта": "sidorov@example.com",
            "номер": "79995554433",
            "роль": role_id,
        },
    )
    assert reg.status_code == 200, reg.json()

    response = client.post(
        "/users/login",
        json={"почта": "sidorov@example.com", "пароль": "mypassword"},
    )
    assert response.status_code == 200, response.json()
    assert "token" in response.json()

    response2 = client.post(
        "/users/login",
        json={"номер": "79995554433", "пароль": "mypassword"},
    )
    assert response2.status_code == 200, response2.json()
    assert "token" in response2.json()


def test_login_wrong_password(client):
    role_id = _create_role(client)

    reg = client.post(
        "/users/registers",
        json={
            "фамилия": "Тест",
            "имя": "Тест",
            "пароль": "correct",
            "почта": "test@test.com",
            "номер": "79991112233",
            "роль": role_id,
        },
    )
    assert reg.status_code == 200, reg.json()

    response = client.post(
        "/users/login",
        json={"почта": "test@test.com", "пароль": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный логин или пароль"


def test_update_user(client):
    role_id = _create_role(client)

    reg_res = client.post(
        "/users/registers",
        json={
            "фамилия": "Обновляев",
            "имя": "Обновляй",
            "пароль": "pass",
            "почта": "update@test.com",
            "номер": "79990001122",
            "роль": role_id,
        },
    )
    assert reg_res.status_code == 200, reg_res.json()
    user_id = reg_res.json()["user"]["id"]

    update_res = client.put(
        f"/users/update?пользователь_id={user_id}",
        json={
            "имя": "НовоеИмя",
            "номер": "79997777777",
            },
    )
    assert update_res.status_code == 200, update_res.json()
    assert update_res.json()["user"]["name"] == "НовоеИмя"
    assert update_res.json()["user"]["number"] == "79997777777"