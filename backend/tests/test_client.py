client_data = {
    "имя": "тест",
    "тип": 1,
    "заметки": "тестовые заметки",
    "контакты": {
        "номер": "87897659076",
        "почта": "test_mail.yandex.ru"
    }
}

def test_create_client(client):
    response = client.post(
        "/clients/client_create",
        json=client_data
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Клиент создан"
    assert response.json()["client"] == {
        "id": 1,
        "name": "тест",
        "type": 1,
        "notes": "тестовые заметки",
        "contacts":  {
            "номер": "87897659076",
            "почта": "test_mail.yandex.ru"
            }
        }

def test_create_empty(client):
    response = client.post(
        "/clients/client_create",
        json={}
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]

def test_update_client(client):
    client.post(
        "/clients/client_create",
        json=client_data
    )

    client_id = 1

    update_res = client.put(
        f"/clients/client_update?клиент_id={client_id}",
        json={
            "имя": "тест",
            "тип": 5,
            "заметки": "",
            "контакты":  {
                "номер": "87777777777",
                "почта": "test_mail.yandex.ru"
            }
        }
    )   

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Клиент успешно обновлен"
    assert update_res.json()["client"] == {
        "id": 1,
        "name": "тест",
        "type": 5,
        "notes": "",
        "contacts":  {
            "номер": "87777777777",
            "почта": "test_mail.yandex.ru"
            }
        }

def test_delete_client(client):
    client.post(
        "/clients/client_create",
        json=client_data
    )

    client_id = 1

    delete_res = client.delete(
        f"/clients/client_delete?клиент_id={client_id}"
        )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Клиент удален"