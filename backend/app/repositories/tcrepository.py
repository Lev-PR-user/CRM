from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import ТипКлиентаM

class Ctcrepository():
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ТипКлиентаM]: 
        return self.db.query(ТипКлиентаM).all()

    def create_type_client(self, TCdata: Dict[str, Any]) -> ТипКлиентаM:
        try:
            type_client_db = ТипКлиентаM(
                тип=TCdata["type"]
            )

            self.db.add(type_client_db)

            self.db.commit()

            self.db.refresh(type_client_db)

            return type_client_db

        except HTTPException:
            self.db.rollback()
            raise

    def update_type_client(self, тип_клиента_id: int, TCupdatedata: Dict[str, Any]) -> ТипКлиентаM:
        try:
            update_type_client_ = self.type_client_by_id(тип_клиента_id)

            if update_type_client_ is None:
                raise HTTPException(status_code=500, detail="Такая услуга не найдена") 

            if "type" in TCupdatedata:
                update_type_client_.тип = TCupdatedata["type"]

            self.db.commit()
            
            self.db.refresh(update_type_client_)

            return update_type_client_

        except HTTPException:
            self.db.rollback()
            raise

    def type_client_by_id(self, тип_клиента_id: int) -> Optional[ТипКлиентаM]:
        try:
            if тип_клиента_id is None:
                return None
            return self.db.query(ТипКлиентаM).filter(ТипКлиентаM.тип_клиента_id == тип_клиента_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def type_client_by_type(self, тип: str) -> Optional[ТипКлиентаM]:
        try:
            if тип is None:
                return None
            return self.db.query(ТипКлиентаM).filter(ТипКлиентаM.тип == тип).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def delete_type_client(self, тип: str, тип_клиента_id: int,) -> bool:
        try:
            db_type_client = self.type_client_by_id(тип_клиента_id) or self.type_client_by_type(тип)

            if db_type_client is None:
                return False

            self.db.delete(db_type_client)

            self.db.commit()

            return True

        except HTTPException:
            self.db.rollback()
            raise