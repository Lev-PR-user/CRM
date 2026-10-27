se_data = {"статус": "активно"}

def test_create_status_equipment(client):
    response = client.post(
        "/status_equipment/status_equipment_create",
        json = se_data
        )

    assert response.status_code == 200
    assert response.json()["message"] == "Статус успешно создан"
    assert response.json()["status"]["status_equipment"] == "активно"

def test_create_duplicate_status_equipment(client):
    client.post(
        "/status_equipment/status_equipment_create",
        json = se_data
    )

    response = client.post(
        "/status_equipment/status_equipment_create",
        json = se_data
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]

def test_create_status_equipment_empty(client):
    response = client.post(
        "/status_equipment/status_equipment_create",
        json = {}
        )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"] 

def test_update_status_equipment(client):
    client.post(
        "/status_equipment/status_equipment_create",
        json = se_data
    )

    status_equipment_id = 1

    update_res = client.put(
        f"/status_equipment/status_equipment_update?статус_оборудования_id={status_equipment_id}",
        json = {
            "статус": "в ремонте"
        }
    )

    assert update_res.status_code == 200    
    assert update_res.json()["message"] == "Статус успешно обновлен"
    assert update_res.json()["status"]["status_equipment"] == "в ремонте"


def test_duplicate_status_equipment(client):
    client.post(
        "/status_equipment/status_equipment_create",
        json = se_data
    )    
    
    client.post(
        "/status_equipment/status_equipment_create",
        json = {
            "статус": "в ремонте"
        }
    )

    status_equipment_id = 1

    update_res = client.put(
        f"/status_equipment/status_equipment_update?статус_оборудования_id={status_equipment_id}",
        json = {
            "статус": "в ремонте"
        }
    )

    assert update_res.status_code == 400
    assert "уже существует" in update_res.json()["detail"]

def test_delete_status_rquipment(client):
    client.post(
        "/status_equipment/status_equipment_create",
        json = se_data
    )    

    status_equipment_id = 1

    status_equipment_delete = client.delete(
       f"/status_equipment/status_equipment_delete?статус_оборудования_id={status_equipment_id}"
    )

    assert status_equipment_delete.status_code == 200
    assert status_equipment_delete.json()["messege"] == "Статус удален"