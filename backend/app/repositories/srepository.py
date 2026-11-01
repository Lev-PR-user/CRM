from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import УслугиM

class Csrepository():
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[УслугиM]:
        return self.db.query(УслугиM).all()

    def create_service(self, servicedata: Dict[str, Any]) -> УслугиM:
        try:
            service_db = УслугиM(
                услуга=servicedata["service"]
            )

            self.db.add(service_db)

            self.db.commit()

            self.db.refresh(service_db)

            return service_db

        except HTTPException:
            self.db.rollback()
            raise

    def update_service(self, serviceupdatedata: Dict[str, Any], услуга_id: Optional[int], услуга: Optional[str]) -> УслугиM:
        try: 
            update_service_db = self.service_by_id(услуга_id) or self.service_by_name(услуга)

            if update_service_db is None:
                raise HTTPException(status_code=500, detail="Такая услуга не найдена") 

            if "service" in serviceupdatedata:
                update_service_db.услуга = serviceupdatedata["service"]

            self.db.commit()

            self.db.refresh(update_service_db)

            return update_service_db

        except HTTPException:
            self.db.rollback()
            raise

    def service_by_id(self, услуга_id: Optional[int]) -> Optional[УслугиM]:
        try: 
            return self.db.query(УслугиM).filter(УслугиM.услуга_id == услуга_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ошибка в базе данных: {str(e)}")

    def delete_service(self, услуга_id: Optional[int], услуга: Optional[str]) -> bool:
        try:
            db_service = self.service_by_id(услуга_id) or self.service_by_name(услуга)

            if db_service is None:
                return False

            self.db.delete(db_service)
            
            self.db.commit()

            return True

        except HTTPException:
            self.db.rollback()
            raise

    def service_by_name(self, услуга: Optional[str]) -> Optional[УслугиM]:
        try: 
            return self.db.query(УслугиM).filter(УслугиM.услуга == услуга).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ошибка в базе данных: {str(e)}")