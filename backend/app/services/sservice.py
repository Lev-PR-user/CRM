from typing import Dict, Any
from ..repositories import Csrepository
from ..validator import Csvalidator

class Csservice():
    def __init__(self, db):
        self.db = db
        self.repository = Csrepository(db)
        self.validator = Csvalidator(self.repository)

    def Screate_service(self, servicedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_create_service(servicedata)

        db_service_data = {
            "service": servicedata["услуга"]
        }

        db_service = self.repository.create_service(db_service_data)

        return {
            "message": "Услуга успешно создана",
            "service": {
                "id": db_service.услуга_id,
                "service": db_service.услуга
            }
        }

    def Supdate_service(self, услуга_id: int, serviceupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_update_status(услуга_id, serviceupdatedata)

        db_service_update_data = {}

        if "услуга" in serviceupdatedata:
            db_service_update_data["service"] = serviceupdatedata["услуга"]

        db_service_update = self.repository.update_service(услуга_id, db_service_update_data)

        return {
            "message": "Услуга успешно обновлена",
            "service": {
                "id": db_service_update.услуга_id,
                "service": db_service_update.услуга
            }
        }


    def Sdelete_service(self, услуга_id: int) -> Dict[str, Any]:

        self.repository.delete_service(услуга_id)

        return {
            "message": "Услуга успешно удалена"
        }
