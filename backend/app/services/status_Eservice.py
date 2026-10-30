from typing import Dict, Any, Optional
from fastapi import HTTPException
from ..repositories import Cstatus_Erepository
from ..validator import Cstatus_Evalidator

class Cstatus_Eservice():
    def __init__(self, db):
        self.db = db
        self.repository = Cstatus_Erepository(db)
        self.validator = Cstatus_Evalidator(self.repository)

    @staticmethod
    def _public(db_status_equipment):
        return {
            "id": db_status_equipment.статус_оборудования_id,
            "status_equipment": db_status_equipment.статус
            }

    def get_all(self):
        return self.repository.get_all()

    def get_status_equipment(self, статус_уведомления_id: Optional[int], статус: Optional[str]):

        if статус_уведомления_id:
            db_status_equipment = self.repository.status_equipment_by_id(статус_уведомления_id)
        elif статус:
            db_status_equipment = self.repository.status_by_name(статус)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска") 

        if db_status_equipment is None:
            raise HTTPException(status_code=400, detail="Такого статуса нет")

        return self._public(db_status_equipment)
    
    def Screate_status_equipment(self, SEdata: Dict) -> Dict[str, Any]:
        
        self.validator.validate_create_status(SEdata)
            
        db_status_equipment_data = {
            "status": SEdata["статус"]
        }

        db_status_equipment = self.repository.create_status_equipment(db_status_equipment_data)

        return {
            "message": "Статус успешно создан",
            "status": self._public(db_status_equipment)
        }


    def Supdate_status_equipment(self, SEdataupdate: Dict, статус_оборудования_id: int) -> Dict[str, Any]:

        self.validator.validate_update_status(статус_оборудования_id, SEdataupdate)

        db_status_equipment_update_data = {}

        if "статус" in SEdataupdate:
            db_status_equipment_update_data["status"] = SEdataupdate["статус"]

        db_status_equipment = self.repository.update_status_equipment(db_status_equipment_update_data, статус_оборудования_id)

        return {
            "message": "Статус успешно обновлен",
            "status": self._public(db_status_equipment)
        }

    def Sdelete_status_equipment(self, статус_оборудования_id: int) -> Dict[str, Any]:
        
        self.repository.delete_status_equipment(статус_оборудования_id)

        return{
            "messege": "Статус удален"
        }
        