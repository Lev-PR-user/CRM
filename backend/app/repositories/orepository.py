from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import ОператорыM

class Corepository():
    def __init__(self, db: Session):
        self.db = db

    def get_all(self,) -> List[ОператорыM]:
        return self.db.query(ОператорыM).all()
    
    def create_operator(self, Odata: Dict[str, Any]) -> ОператорыM:
        try:
            operator_db = ОператорыM(
            пользователь=Odata["user"],
            локации=Odata["location"],
            график=Odata["schedule"]
            )

            self.db.add(operator_db)

            self.db.commit()

            self.db.refresh(operator_db)

            return operator_db
        
        except HTTPException:
            self.db.rollback()
            raise

    def update_operator(self, оператор_id: int, Oupdatedata: Dict[str, Any]) -> ОператорыM:
        try:
            update_operators_db = self.operator_by_id(оператор_id)

            if update_operators_db is None:

                raise HTTPException(status_code=500, detail="Такой оператор не найдена")

            if "user" in Oupdatedata:
                update_operators_db.пользователь = Oupdatedata["user"]
            if "location" in Oupdatedata: 
                update_operators_db.локации = Oupdatedata["location"]   
            if "shedule" in Oupdatedata:
                update_operators_db.график = Oupdatedata["shedule"]

            self.db.commit()

            self.db.refresh(update_operators_db)

            return update_operators_db
        
        except HTTPException:
            self.db.rollback()
            raise

    def operator_by_id(self, оператор_id: Optional[int]) -> Optional[ОператорыM]:
        try:
            if оператор_id is None:
                return None
            return self.db.query(ОператорыM).filter(ОператорыM.оператор_id == оператор_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def operator_by_location(self, локации: Optional[str]) -> Optional[ОператорыM]:
        try:
            if локации is None:
                return None
            for op in self.db.query(ОператорыM).all():
                if op.локации and локации in op.локации:
                    return op
                return None        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def delete_operator(self, оператор_id: int) -> bool:
        try:
            operator_db = self.operator_by_id(оператор_id)

            if operator_db is None:
                return False

            self.db.delete(operator_db)
            
            self.db.commit()

            return True
        
        except HTTPException:
            
            self.db.rollback()
            
            raise