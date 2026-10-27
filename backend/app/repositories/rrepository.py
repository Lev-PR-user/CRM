from typing import Dict, Any, Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import Base, РолиM

class Crrepository():

    def __init__(self, db: Session):
        self.db = db

    def create_role(self, roledata: Dict[str, Any]) -> РолиM:
        try:
            role_db = РолиM(
                название_роли=roledata["name"],
                описание=roledata["description"]
            )

            self.db.add(role_db)
            
            self.db.commit()

            self.db.refresh(role_db)

            return role_db
            
        except HTTPException:
            self.db.rollback()
            raise

    def update_role(self, роль_id: int, updateroledata: Dict[str, Any]) -> РолиM:
        try:
            update_role_db = self.role_by_id(роль_id)

            if update_role_db is None:
                raise HTTPException(status_code=500, detail="Такая роль не найдена")

            if "name" in updateroledata:
                update_role_db.название_роли = updateroledata["name"]
            if "description" in updateroledata:
                update_role_db.описание = updateroledata["description"]

            self.db.commit()

            self.db.refresh(update_role_db)

            return update_role_db

        except HTTPException:
            self.db.rollback()
            raise

    def delete_role(self, роль_id: int) -> bool:
        try:
            db_role = self.role_by_id(роль_id)
            
            if db_role is None:

                return False

            self.db.delete(db_role)

            self.db.commit()

            return True
        
        except HTTPException:
            self.db.rollback()
            raise

    def role_by_id(self, роль_id: int) -> Optional[РолиM]:
        try:
            return self.db.query(РолиM).filter(РолиM.роль_id == роль_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def role_by_name(self, название_роли: str) -> Optional[РолиM]:
        try: 
            return self.db.query(РолиM).filter(РолиM.название_роли == название_роли).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Такой роли нет в базе данных: {str(e)}")