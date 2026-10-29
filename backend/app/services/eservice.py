from typing import Dict, Any
from ..repositories import Cerepository
from ..validator import Cevalidator

class Ceservice():
    def __init__(self, db):
        self.db = db
        self.repository = Cerepository(db)
        self.validator = Cevalidator(self.repository)

    def Screate_equipment(self, equipmentdata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_create_equipment(equipmentdata)

        db_equipment_data ={
            "model": equipmentdata["модель"],
            "series": equipmentdata["серия"],
            "status": equipmentdata["статус"],
            "location": equipmentdata["расположение"]
        }

        db_equipment = self.repository.create_equipment(db_equipment_data)

        return {
            "message": "Оборудование создано",
            "eqiupment": {
                "id": db_equipment.оборудование_id,
                "model": db_equipment.модель,
                "series": db_equipment.серия,
                "status": db_equipment.статус,
                "location": db_equipment.расположение
            }
        }

    def Supdate_equipment(self, equipmentupdatedata: Dict[str, Any], оборудование_id: int) -> Dict[str, Any]:

        db_equipment_update_data = {}

        if "модель" in equipmentupdatedata:
            db_equipment_update_data["model"] = equipmentupdatedata["модель"]
        if "серия" in equipmentupdatedata:
            db_equipment_update_data["series"] = equipmentupdatedata["серия"]
        if "статус" in equipmentupdatedata:
            db_equipment_update_data["status"] = equipmentupdatedata["статус"]
        if "расположение" in equipmentupdatedata:
            db_equipment_update_data["location"] = equipmentupdatedata["расположение"]

        db_equipment_update = self.repository.update_equipment(db_equipment_update_data, оборудование_id)

        return {
            "message": "оборудование обновлено",
            "eqiupment": {
                "id": db_equipment_update.оборудование_id,
                "model": db_equipment_update.модель,
                "series": db_equipment_update.серия,
                "status": db_equipment_update.статус,
                "location": db_equipment_update.расположение
            }
        }

    def Sdelete_equipment(self, оборудование_id: int) -> Dict[str, Any]:
        self.repository.equipment_by_id(оборудование_id)

        self.repository.delete_equipment(оборудование_id)

        return {
            "message": "Оборудование удалено"
        }
