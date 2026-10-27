from typing import Dict, Any
from ..repositories import Ccrepository
from ..validator import Ccvalidator

class Ccservice():
    def __init__(self, db):
        self.db = db
        self.repository = Ccrepository(db)
        self.validator = Ccvalidator(self.repository)

    def create_client(self, clientdata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_create_client(clientdata)

        db_client_data = {
            "name": clientdata["имя"],
            "type": clientdata["тип"],
            "notes": clientdata["заметки"],
            "contacts": clientdata["контакты"]
        }

        db_client = self.repository.create_client(db_client_data)

        return {
            "message": "Клиент создан",
            "Client": {
                "id": db_client.клиент_id,
                "name": db_client.имя,
                "type": db_client.тип,
                "notes": db_client.заметки,
                "contacts": db_client.контакты
            }
        }

    def update_client(self, клиент_id: int, clientupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_update_client(clientupdatedata)

        db_client_update_data = {}

        if "имя" in clientupdatedata:
            db_client_update_data["name"] = clientupdatedata["имя"]
        if "тип" in clientupdatedata:
            db_client_update_data["type"] = clientupdatedata["имя"]
        if "заметки" in clientupdatedata:
            db_client_update_data["notes"] = clientupdatedata["имя"]
        if "контакты" in clientupdatedata:
            db_client_update_data["contacts"] = clientupdatedata["имя"]

        db_client_update = self.repository.update_client(клиент_id, db_client_update_data)

        return {
            "message": "Клиент успешно обновлен",
            "client": {
                "id": db_client_update.клиент_id,
                "name": db_client_update.имя,
                "type": db_client_update.тип,
                "notes": db_client_update.заметки,
                "contacts": db_client_update.контакты
            }
        }

    def delete_client(self, клиент_id: int) -> Dict[str, Any]:

        self.repository.delete_client(клиент_id)

        return {
            "message": "Клиент удален"
        }