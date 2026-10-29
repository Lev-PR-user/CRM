from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import ОборудованиеM 

class Cerepository():
    def __init__(self, db: Session):
        self.db = db

    def create_equipment(self, equipmentdata: Dict[str, Any]) -> ОборудованиеM:
        try:
            equipment_db = ОборудованиеM(
                модель=equipmentdata["model"],
                серия=equipmentdata["series"],
                статус=equipmentdata["status"],
                расположение=equipmentdata["location"]
            )

            self.db.add(equipment_db)

            self.db.commit()

            self.db.refresh(equipment_db)

            return equipment_db

        except HTTPException:
            self.db.rollback()
            raise

    def update_equipment(self, equipmentupdatedata: Dict[str, Any], оборудование_id: int) -> ОборудованиеM:
        try:
            update_equipment_db = self.equipment_by_id(оборудование_id)

            if update_equipment_db is None:
                raise HTTPException(status_code=500, detail="Такое оборудование не найдено")

            if "model" in equipmentupdatedata:
                update_equipment_db.модель = equipmentupdatedata["model"]        
            if "series" in equipmentupdatedata:
                update_equipment_db.серия = equipmentupdatedata["series"]        
            if "status" in equipmentupdatedata:
                update_equipment_db.статус = equipmentupdatedata["status"]        
            if "location" in equipmentupdatedata:
                update_equipment_db.расположение = equipmentupdatedata["location"]

            self.db.commit()

            self.db.refresh(update_equipment_db)

            return update_equipment_db

        except HTTPException:
            self.db.rollback()
            raise

    def equipment_by_id(self, оборудование_id: int) -> Optional[ОборудованиеM]:
        try: 
            return self.db.query(ОборудованиеM).filter(ОборудованиеM.оборудование_id == оборудование_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def delete_equipment(self, оборудование_id: int) -> bool:
        try: 

            db_equipment = self.equipment_by_id(оборудование_id)

            if db_equipment is None:
                return False

            self.db.delete(db_equipment)

            self.db.commit()

            return True

        except HTTPException:
            self.db.rollback()
            raise

            