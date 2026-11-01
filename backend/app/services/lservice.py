from typing import Dict, Any, Optional
from fastapi import HTTPException
from ..repositories import Clrepository
from ..validator import Clvalidator

class Clservice():
    def __init__(self, db):
        self.db = db
        self.repository = Clrepository(db)
        self.validator = Clvalidator(self.repository)

    @staticmethod
    def _public(db_location) -> Dict[str, Any]:
        return {
            "id": db_location.локация_id,
            "name": db_location.название,
            "address": db_location.адрес,
            "openning_hours": db_location.часы_работы
        }

    def Sget_all(self):
        return [self._public(l) for l in self.repository.get_all()]

    def Sget_location(self, локация_id: Optional[int], название: Optional[str], адрес: Optional[str]):

        if локация_id:
            db_location = self.repository.location_by_id(локация_id)
        elif название:
            db_location = self.repository.location_by_name(название)
        elif адрес:
            db_location = self.repository.location_by_address(адрес)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска")

        if db_location is None:
            raise HTTPException(status_code=400, detail="Такой локации нет")

        return self._public(db_location)


    def Screate_location(self, locationdata: Dict[str, Any]) -> Dict[str, Any]:
        self.validator.validate_create_location(locationdata)

        db_location_data = {
            "name": locationdata["название"],
            "address": locationdata["адрес"],
            "openning_hours": locationdata["часы_работы"]
        }

        db_location = self.repository.create_location(db_location_data)

        return{
            "message": "Локация успешно добавлена",
            "location": self._public(db_location)
        }

    def Supdate_location(self, локация_id: int, locationupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.valifate_update_location(локация_id, locationupdatedata)

        db_location_update_data = {}

        if "название" in locationupdatedata:
            db_location_update_data["name"] = locationupdatedata["название"]
        if "адрес" in locationupdatedata:
            db_location_update_data["address"] = locationupdatedata["адрес"]
        if "часы_работы" in locationupdatedata:
            db_location_update_data["openning_hours"] = locationupdatedata["часы_работы"]


        db_location = self.repository.update_location(локация_id, db_location_update_data)

        return {
            "message": "Локация успешно обновлена",
            "location": self._public(db_location)
        }

    def Sdelete_location(self, локация_id: int) -> Dict[str, Any]:

        self.repository.delete_location(локация_id)

        return {
            "message": "локация удалена"
        }