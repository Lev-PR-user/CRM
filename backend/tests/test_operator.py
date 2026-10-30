from .data import operator_data

def test_create_operators(client):
    response = client.post(
        "/operators/operator_create", 
        json=operator_data
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оператор успешно создан"
    assert response.json()["operator"] == {
        "id": 1,
        "user": 1,
        "locationn": [
            "пушкинская д 56",
            "пушкинская д 6"
        ],
        "shedule": {
            "пн-пт": "9:00-18:00",
            "вс": "10:00-16:00"
            }
        }
     

def test_create_operators_empty(client):
    response = client.post(
        "/operators/operator_create", 
        json={}
    )

    assert response.status_code == 400
    assert "обязательны для заполнения" in response.json()["detail"]

def test_update_operators(client):
    client.post(
        "/operators/operator_create", 
        json=operator_data
    )

    operators_id = 1

    update_res = client.put(
        f"/operators/operator_update?оператор_id={operators_id}",
        json={
            "пользователь": 1,
            "локации": [
                "пушкинская д 56",
                ],
                "график": {
                    "пн-пт": "9:00-11:00",
                    }
                }
    )


    assert update_res.status_code == 200, update_res.json()
    assert update_res.json()["message"] == "Оператор успешно обновлен"
    assert update_res.json()["operator"] == {
        "id": 1,
        "user": 1,
        "locationn": [
            "пушкинская д 56"
            ],
        "shedule": {
            "пн-пт": "9:00-11:00"
            }
        }

def test_delete_operatos(client):
    client.post(
        "/operators/operator_create", 
        json=operator_data
    )

    operators_id = 1

    delete_res = client.delete(
        f"/operators/operator_delete?оператор_id={operators_id}"
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Оператор удален"
