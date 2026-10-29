service_data = {
    "услуга": "сканирование помещения"
}

def test_create_service(client):
    response = client.post(
        "/services/service_create",
        json=service_data
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Услуга успешно создана"
    assert response.json()["service"] == {
        "id": 1,
        "service": "сканирование помещения"
    }

def test_create_duplicate_service(client):
    client.post(
        "/services/service_create",
        json=service_data
    )

    response = client.post(
        "/services/service_create",
        json=service_data
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]

def test_create_service_empty(client):
    response = client.post(
        "/services/service_create",
        json={}
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]

def test_update_service(client):
    client.post(
        "/services/service_create",
        json=service_data
    )

    service_id = 1

    update_res = client.put(
        f"/services/service_update?услуга_id={service_id}",
        json= {
               "услуга": "test"
        }
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Услуга успешно обновлена"
    assert update_res.json()["service"] == {
        "id": 1,
        "service": "test"
    }

def test_update_buplicate_service(client):
    client.post(
        "/services/service_create",
        json=service_data
    )

    client.post(
        "/services/service_create",
        json={
            "услуга": "test"
            }
    )


    service_id = 1

    update_res = client.put(
        f"/services/service_update?услуга_id={service_id}",
        json= {
            "услуга": "test"
            }
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]

def test_delete_service(client):
    client.post(
        "/services/service_create",
        json={
            "услуга": "test"
            }
    )


    service_id = 1 

    delete_res = client.delete(
        f"/services/service_delete?услуга_id={service_id}"
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Услуга успешно удалена"
