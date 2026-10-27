from typing import Dict, Any, Optional
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import Base, ПользователиM

class CuRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, userdata: Dict[str, Any]) -> ПользователиM:
        try: 

            user_db = ПользователиM(
                фамилия=userdata["secondname"],
                имя=userdata["name"],
                пароль=userdata["password"],
                отчество=userdata["middlename"],
                название_организации=userdata["name_organition"],
                почта=userdata["email"],
                номер=userdata["number"],
                роль=userdata["role"]
                )
            
            self.db.add(user_db)
            
            self.db.commit()
            
            self.db.refresh(user_db)

            return user_db

        except HTTPException:
            self.db.rollback()
            raise
           
    def user_by_email(self, email: str) -> Optional[ПользователиM]:
        try: 
            return (self.db.query(ПользователиM).filter(ПользователиM.почта == email).first())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ошибка в базе данных: {str(e)}")
          
    def user_by_number(self, number: str) -> Optional[ПользователиM]:
        try: 
            return (self.db.query(ПользователиM).filter(ПользователиM.номер == number).first())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ошибка в базе данных: {str(e)}")

    def update_user(self, пользователь_id: int, updateuserdata: Dict[str, Any]) -> ПользователиM:
        try:
            update_user_db = self.user_by_id(пользователь_id)
            
            if update_user_db is None:
                raise HTTPException(status_code=404, detail="Пользователь не нйден")
            
            if "secondname" in updateuserdata:
                update_user_db.фамилия = updateuserdata["secondname"]
            if "name" in updateuserdata:
                update_user_db.имя = updateuserdata["name"]
            if "password" in updateuserdata:
                update_user_db.пароль = updateuserdata["password"]
            if "middlename" in updateuserdata:
                update_user_db.отчество = updateuserdata["middlename"]
            if "name_organition" in updateuserdata:
                update_user_db.название_организации = updateuserdata["name_organition"]
            if "email" in updateuserdata:
                update_user_db.почта = updateuserdata["email"]
            if "number" in updateuserdata:
                update_user_db.номер = updateuserdata["number"]

            self.db.commit()

            self.db.refresh(update_user_db)

            return update_user_db
        
        except HTTPException:
            self.db.rollback()
            raise
    
    def user_by_id(self, пользователь_id: int) -> Optional[ПользователиM]:
        try: 
            return self.db.query(ПользователиM).filter(ПользователиM.пользователь_id == пользователь_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ошибка в базе данных: {str(e)}")

    def delete_user(self, пользователь_id: int) -> bool:
        try:
            db_user = self.user_by_id(пользователь_id)

            if db_user is None:
                return False

            self.db.delete(db_user)

            self.db.commit()
            return True
        
        except HTTPException:
            self.db.rollback()
            raise