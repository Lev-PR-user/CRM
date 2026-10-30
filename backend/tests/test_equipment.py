from .data import equipment_data

def test_create_equipmnet(client):
    response = client.post(
        "/equipment/create_equipment",
        json=equipment_data
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"
    assert response.json()["eqiupment"] == {
        "id": 1,
        "model": "Sdt",
        "series": "345wd",
        "status": 1,
        "location": 1
    }

def test_create_equipmnet_empty(client):
    response = client.post(
        "/equipment/create_equipment",
        json={}
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]

def test_update_equipment(client):
    client.post(
        "/equipment/create_equipment",
        json=equipment_data
    )

    equipment_id = 1

    update_res = client.put(
        f"/equipment/update_equipment?оборудование_id={equipment_id}",
        json={
            "модель": "Sdt",
            "серия": "345wd",
            "статус": 3,
            "расположение": 2
        }
    )

    assert update_res.status_code == 200,  f"status={update_res.status_code}, body={update_res.text}"
    assert update_res.json()["message"] == "оборудование обновлено"
    assert update_res.json()["eqiupment"] == {
        "id": 1,
        "model": "Sdt",
        "series": "345wd",
        "status": 3,
        "location": 2
    }

def test_delete_equipment(client):

    client.post(
        "/equipment/create_equipment",
        json=equipment_data
    )

    equipment_id = 1

    delete_res = client.delete(
        f"/equipment/delete_equipment?оборудование_id={equipment_id}"
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Оборудование удалено"