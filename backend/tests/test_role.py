from .data import role_data_admin, role_data_user, role_data

def test_create_role(client):
    response = client.post(
        "/roles/createrole",  
        json=role_data_admin
    )
    assert response.status_code == 200
    assert response.json()["Message"] == "роль создана успешно"
    assert response.json()["role"]["name"] == "admin"


def test_create_duplicate_role(client):
    
    
    client.post("/roles/createrole", json=role_data)
    
    response = client.post("/roles/createrole", json=role_data)
    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]

def test_create_role_empty(client):
    response = client.post(
        "/roles/createrole",  
        json = {})
    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]

def test_update_role(client):
    client.post(
        "/roles/createrole", 
        json=role_data_user
    )
    
    role_id = 1 

    update_res = client.put(
        f"/roles/update?роль_id={role_id}",
        json={"название_роли": "superuser", "описание": "Обновленное описание"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Роль успешно обновлена"
    assert update_res.json()["role"]["name"] == "superuser"


def test_delete_role(client):
    client.post(
        "/roles/createrole", 
        json=role_data_user
    )
    role_id = 1

    delete_res = client.delete(f"/roles/delete?роль_id={role_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Роль успешно удалена"