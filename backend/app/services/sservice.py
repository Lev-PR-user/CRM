from typing import Dict, Any, Optional
from fastapi import HTTPException
from ..repositories import Csrepository
from ..validator import Csvalidator

class Csservice():
    def __init__(self, db):
        self.db = db
        self.repository = Csrepository(db)
        self.validator = Csvalidator(self.repository)

    @staticmethod
    def _public(db_service) -> Dict[str, Any]:
        return {
            "id": db_service.услуга_id,
            "service": db_service.услуга
            }

    def Sget_all(self):
        return [self._public(s) for s in self.repository.get_all()]

    def Sget_location(self, услуга_id: Optional[int], услуга: Optional[str]):

        if услуга_id:
            db_service = self.repository.service_by_id(услуга_id)
        if услуга:
            db_service = self.repository.service_by_name(услуга)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска")
        
        if db_service is None:
            raise HTTPException(status_code=400, detail="Такой услуги нет")

        return self._public(db_service)

    def Screate_service(self, servicedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_create_service(servicedata)

        db_service_data = {
            "service": servicedata["услуга"]
        }

        db_service = self.repository.create_service(db_service_data)

        return {
            "message": "Услуга успешно создана",
            "service": self._public(db_service)
        }

    def Supdate_service(self, услуга_id: int, serviceupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_update_status(услуга_id, serviceupdatedata)

        db_service_update_data = {}

        if "услуга" in serviceupdatedata:
            db_service_update_data["service"] = serviceupdatedata["услуга"]

        db_service = self.repository.update_service(услуга_id, db_service_update_data)

        return {
            "message": "Услуга успешно обновлена",
            "service":self._public(db_service)
        }


    def Sdelete_service(self, услуга_id: int) -> Dict[str, Any]:

        self.repository.delete_service(услуга_id)

        return {
            "message": "Услуга успешно удалена"
        }
