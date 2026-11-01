from data import user_data, user_login_number

def _register_and_login(client, register_data, login_data):
    reg = client.post("/pusers/registers", json=register_data)
    assert reg.status_code == 200, reg.json()

    login = client.post("/pusers/login", json=login_data)
    assert login.status_code == 200, login.json()

    token = login.json()["token"]
    user = login.json()["user"]
    return user, {"Authorization": f"Bearer {token}"}