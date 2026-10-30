from typing import Dict, Any, Optional
from fastapi import HTTPException
from ..repositories import Ctcrepository
from ..validator import Сtcvalidator

class Ctcservice():
    def __init__(self, db):
        self.db = db
        self.repository = Ctcrepository(db)
        self.validator = Сtcvalidator(self.repository)

    @staticmethod
    def _public(db_type_client) -> Dict[str, Any]:
        return {
            "id": db_type_client.тип_клиента_id,
            "type": db_type_client.тип
            }

    def get_all(self):
        return [self._public(tc) for tc in self.repository.get_all()]

    def get_type_client(self, тип: Optional[str], тип_клиента_id: Optional[int]):

        if тип:
            db_type_client = self.repository.type_client_by_type(тип)
        elif тип_клиента_id:
            db_type_client = self.repository.type_client_by_id(тип_клиента_id)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска")

        if db_type_client is None:
            raise HTTPException(status_code=400, detail="Такого типа нет") 

        return self._public(db_type_client)

    def Screate_type_client(self, TCdata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_create_type_client(TCdata)
        
        db_type_client_data = {
            "type": TCdata["тип"]
        }

        db_type_client = self.repository.create_type_client(db_type_client_data)

        return {
            "message": "Тип клиента успешно добавлен",
            "type_client": self._public(db_type_client)
        }

    def Supdate_type_client(self, тип, тип_клиента_id, TCupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_update_type_client(тип_клиента_id, TCupdatedata)

        db_type_client_update_data = {}

        if "тип" in TCupdatedata:
            db_type_client_update_data["type"] = TCupdatedata["тип"]

        db_type_client = self.repository.update_type_client(тип, тип_клиента_id, db_type_client_update_data)

        return {
            "message": "Тип клиента обновлен", 
            "type_client": self._public(db_type_client)
        }

    def Sdelete_type_client(self, тип_клиента_id, тип)  -> Dict[str, Any]:

        self.repository.delete_type_client(тип, тип_клиента_id)

        return {
            "message": "Тип успешно удален"
        }
