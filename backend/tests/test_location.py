from .data import location_data

def test_create_location(client):

    response = client.post(
        "/locations/location_create",
        json=location_data
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Локация успешно добавлена"
    assert response.json()["location"] == {
        "id": 1, 
        "name": "тексел", 
        "address": "пушкинская д 6" ,
        "openning_hours": {
            "пн-пт": "09:00-18:00",
            "сб": "10:00-15:00",
            "вс": "выходной",
            }}

def test_create_duplicate_location(client):
    client.post(
        "/locations/location_create",
        json=location_data
    )

    response = client.post(
        "/locations/location_create",
        json=location_data
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]

def test_create_location_empty(client):
    response = client.post(
        "/locations/location_create",
        json={}
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]

def test_update_location(client):
    client.post(
        "/locations/location_create",
        json = location_data
    )

    location_id = 1

    update_res = client.put(
        f"/locations/location_update?локация_id={location_id}",
        json={ 
            "название": "тексел", 
            "адрес": "пушкинская д 6" ,
            "часы_работы": {
                "пн-пт": "09:00-18:00",
                "сб": "10:00-15:00",
                "вс": "выходной"
            }
        }
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Локация успешно обновлена"
    assert update_res.json()["location"] == { 
        "id": 1,
        "name": "тексел", 
        "address": "пушкинская д 6" ,
        "openning_hour": {
            "пн-пт": "09:00-18:00",
            "сб": "10:00-15:00",
            "вс": "выходной",
            }
        }

def test_update_duplicate_location(client):
    client.post(
        "/locations/location_create",
        json = location_data
    )

    client.post(
        f"/locations/location_create",
        json = { 
            "название": "тексел", 
            "адрес": "тестовая д 6" ,
            "часы_работы": {
                "пн-пт": "09:00-21:00",
                "сб": "10:00-14:00",
                "вс": "выходной"
            }
        }
    )

    location_id = 1

    update_res = client.put(
        f"/locations/location_update?локация_id={location_id}",
        json={ 
            "название": "тексел", 
            "адрес": "тестовая д 6" ,
            "часы_работы": {
                "пн-пт": "09:00-21:00",
                "сб": "10:00-14:00",
                "вс": "выходной"
            }
        }
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]

def test_delete_location(client):
    client.post(
        f"/locations/location_create",
        json = location_data
    )


    location_id = 1

    delete_res = client.delete(
        f"/locations/location_delete?локация_id={location_id}")

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "локация удалена"