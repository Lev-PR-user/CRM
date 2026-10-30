from typing import Dict, Any, List
from fastapi import HTTPException
from ..repositories import Ccrepository
from ..validator import Ccvalidator

class Ccservice():
    def __init__(self, db):
        self.db = db
        self.repository = Ccrepository(db)
        self.validator = Ccvalidator(self.repository) 

    @staticmethod
    def _public(db_client) -> Dict[str, Any]:
        return {
            "id": db_client.клиент_id,
            "name": db_client.имя,
            "type": db_client.тип,
            "notes": db_client.заметки,
            "contacts": db_client.контакты
        }

    def Sget_all(self) -> List[Dict[str, Any]]:
        return [self._public(c) for c in self.repository.get_all()]

    def Sget_client(self, клиент_id, имя) -> Dict[str, Any]:

        if клиент_id:
            db_client = self.repository.client_by_id(клиент_id)
        elif имя:
            db_client = self.repository.client_by_name(имя)
        else: 
            raise HTTPException(status_code=400, detail="Введите данные для поиска")

        if db_client is None:
            raise HTTPException(status_code=400, detail="Такого клиента нет")

        return self._public(db_client)

    def Screate_client(self, clientdata: Dict[str, Any]) -> Dict[str, Any]:

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
            "client": self._public(db_client)
        }

    def Supdate_client(self, клиент_id: int, clientupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        db_client_update_data = {}

        if "имя" in clientupdatedata:
            db_client_update_data["name"] = clientupdatedata["имя"]
        if "тип" in clientupdatedata:
            db_client_update_data["type"] = clientupdatedata["тип"]
        if "заметки" in clientupdatedata:
            db_client_update_data["notes"] = clientupdatedata["заметки"]
        if "контакты" in clientupdatedata:
            db_client_update_data["contacts"] = clientupdatedata["контакты"]

        db_client = self.repository.update_client(клиент_id, db_client_update_data)

        return {
            "message": "Клиент успешно обновлен",
            "client": self._public(db_client)
        }

    def Sdelete_client(self, клиент_id: int) -> Dict[str, Any]:

        self.repository.delete_client(клиент_id)

        return {
            "message": "Клиент удален"
        }