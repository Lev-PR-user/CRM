from typing import Dict, Any, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import СтатусОборудованияM

class Cstatus_Erepository():
    def __init__(self, db: Session):
        self.db = db

    def create_status_equipment(self, SEdata: Dict[str, Any]) -> СтатусОборудованияM:
        try: 
            status_equipment_db = СтатусОборудованияM(
                статус=SEdata["status"]
            )

            self.db.add(status_equipment_db)

            self.db.commit()

            self.db.refresh(status_equipment_db)

            return status_equipment_db
        except HTTPException:
            self.db.rollback()
            raise

    def update_status_equipment(self, SEdataupdate: Dict[str, Any], статус_оборудования_id: int) -> СтатусОборудованияM:
        try: 
            update_status_equipment_db = self.status_equipment_by_id(статус_оборудования_id)

            if update_status_equipment_db is None:
                raise HTTPException(status_code=500, detail="Такой статус не найдена")

            if "status" in SEdataupdate:
                update_status_equipment_db.статус = SEdataupdate["status"]

            self.db.commit()

            self.db.refresh(update_status_equipment_db)

            return update_status_equipment_db

        except HTTPException:
            self.db.rollback()
            raise

    def status_equipment_by_id(self, статус_оборудования_id: int) -> Optional[СтатусОборудованияM]:
        try: 
            return self.db.query(СтатусОборудованияM).filter(СтатусОборудованияM.статус_оборудования_id == статус_оборудования_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def delete_status_equipment(self, статус_оборудования_id: int) -> bool:
        try: 

            db_status_equipment = self.status_equipment_by_id(статус_оборудования_id)

            if db_status_equipment is None:
                return False

            self.db.delete(db_status_equipment)

            self.db.commit()

            return True
        except HTTPException:
            self.db.rollback()
            raise

    def status_by_name(self, статус: str) -> Optional[СтатусОборудованияM]:
        try:
            return self.db.query(СтатусОборудованияM).filter(СтатусОборудованияM.статус == статус).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")
    
