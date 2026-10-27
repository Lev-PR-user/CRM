from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import ЛокацииM

class Clrepository():
    def __init__(self, db: Session):
        self.db = db

    def create_location(self, locationdata: Dict[str, Any]) -> ЛокацииM:
        try:

            location_db = ЛокацииM(
                название= locationdata["name"],
                адрес= locationdata["address"],
                часы_работы= locationdata["openning_hours"]
            )

            self.db.add(location_db)

            self.db.commit()

            self.db.refresh(location_db)

            return location_db

        except HTTPException:
            self.db.rollback()
            raise

    def update_location(self, локация_id: int, locationupdatedata: Dict[str, Any]) -> ЛокацииM:
        try: 
                location_db = self.location_by_id(локация_id)

                if location_db is None:
                    raise HTTPException(status_code=500, detail="Такой локации нет")


                if "name" in locationupdatedata:
                    location_db.название = locationupdatedata["name"]
                if "address" in locationupdatedata:
                    location_db.адрес = locationupdatedata["address"]
                if "openning_hours" in locationupdatedata:
                    location_db.часы_работы = locationupdatedata["openning_hours"]

                self.db.commit()

                self.db.refresh(location_db)

                return location_db

        except HTTPException:
            self.db.rollback()
            raise

    def location_by_id(self, локация_id: int) -> Optional[ЛокацииM]:
        try:
            return self.db.query(ЛокацииM).filter(ЛокацииM.локация_id == локация_id).first()
        except HTTPException:
            self.db.rollback()
            raise
        

    def delete_location(self, локация_id: int) -> bool:
        try:
            location_db = self.location_by_id(локация_id)

            if location_db is None:
                return False

            self.db.delete(location_db)

            self.db.commit()

            return True
        
        except HTTPException:
            self.db.rollback()
            raise

    def location_by_address(self, адрес: str) -> Optional[ЛокацииM]:
        try: 
            return self.db.query(ЛокацииM).filter(ЛокацииM.адрес == адрес).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Такого адреса нет: {str(e)}")
        