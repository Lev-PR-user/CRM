from typing import Dict, Any
from ..repositories import Cstatus_Erepository
from ..validator import Cstatus_Evalidator

class Cstatus_Eservice():
    def __init__(self, db):
        self.db = db
        self.repository = Cstatus_Erepository(db)
        self.validator = Cstatus_Evalidator(self.repository)
    
    def Screate_status_equipment(self, SEdata: Dict) -> Dict[str, Any]:
        
        self.validator.validate_create_status(SEdata)
            
        db_status_equipment_data = {
            "status": SEdata["статус"]
        }

        db_status_equipment = self.repository.create_status_equipment(db_status_equipment_data)

        return {
            "message": "Статус успешно создан",
            "status": {
                "id": db_status_equipment.статус_оборудования_id,
                "status_equipment": db_status_equipment.статус
            }
        }


    def Supdate_status_equipment(self, SEdataupdate: Dict, статус_оборудования_id: int) -> Dict[str, Any]:

        self.validator.validate_update_status(статус_оборудования_id, SEdataupdate)

        db_status_equipment_update_data = {}

        if "статус" in SEdataupdate:
            db_status_equipment_update_data["status"] = SEdataupdate["статус"]

        db_status_equipment_update = self.repository.update_status_equipment(db_status_equipment_update_data, статус_оборудования_id)

        return {
            "message": "Статус успешно обновлен",
            "status": {
                    "id": db_status_equipment_update.статус_оборудования_id,
                    "status_equipment": db_status_equipment_update.статус
                }
        }

    def Sdelete_status_equipment(self, статус_оборудования_id: int) -> Dict[str, Any]:
        
        self.repository.delete_status_equipment(статус_оборудования_id)

        return{
            "messege": "Статус удален"
        }
        