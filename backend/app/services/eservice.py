from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from ..repositories import Cerepository
from ..validator import Cevalidator

class Ceservice():
    def __init__(self, db):
        self.db = db
        self.repository = Cerepository(db)
        self.validator = Cevalidator(self.repository)

    @staticmethod
    def _public(db_equipment) -> Dict[str, Any]:
        return {
            "id": db_equipment.оборудование_id,
            "model": db_equipment.модель,
            "series": db_equipment.серия,
            "status": db_equipment.статус,
            "location": db_equipment.расположение
        }

    def Sget_all(self) -> List[Dict[str, Any]]:
        return [self._public(e) for e in self.repository.get_all()]

    def Sget_equipment(self, оборудование_id: Optional[int], модель: Optional[str], серия: Optional[str]):
                
        if оборудование_id:
           equipment_db =  self.repository.equipment_by_id(оборудование_id)
        elif модель is not None:
            equipment_db = self.repository.equipment_by_model(модель)
        elif серия is not None:
            equipment_db = self.repository.equipment_by_series(серия)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска")

        if equipment_db is None:
            raise HTTPException(status_code=400, detail="Такого клиента нет")

        return self._public(equipment_db)

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
            "eqiupment": self._public(db_equipment)
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

        db_equipment = self.repository.update_equipment(db_equipment_update_data, оборудование_id)

        return {
            "message": "оборудование обновлено",
            "eqiupment": self._public(db_equipment)
        }

    def Sdelete_equipment(self, оборудование_id: int) -> Dict[str, Any]:
        self.repository.equipment_by_id(оборудование_id)

        self.repository.delete_equipment(оборудование_id)

        return {
            "message": "Оборудование удалено"
        }
