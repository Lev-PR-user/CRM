from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import КлиентыM

class Ccrepository():
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, clientdata: Dict[str, Any]) -> КлиентыM:
        try: 

            client_db = КлиентыM(
                имя=clientdata["name"],
                тип=clientdata["type"],
                заметки=clientdata["notes"],
                контакты=clientdata["contacts"]
            )

            self.db.add(client_db)

            self.db.commit()

            self.db.refresh(client_db)

            return client_db

        except HTTPException:
            self.db.rollback()
            raise


    def update_client(self, клиент_id: int, clientupdatedata: Dict[str, Any]) -> КлиентыM:
        try:
            client_update_db = self.client_by_id(клиент_id)

            if client_update_db is None:
                raise HTTPException(status_code=500, detail="Такой клиент не найдена")

            if "name" in clientupdatedata:
                client_update_db.имя = clientupdatedata["name"]
            if "type" in clientupdatedata:
                client_update_db.тип = clientupdatedata["type"]
            if "notes" in clientupdatedata:
                client_update_db.заметки = clientupdatedata["notes"]
            if "contacts" in clientupdatedata:
                client_update_db.контакты = clientupdatedata["contacts"]

            self.db.commit()

            self.db.refresh(client_update_db)

            return client_update_db
        
        except HTTPException:
            self.db.rollback()
            raise


    def client_by_id(self, клиент_id: int) -> Optional[КлиентыM]:
        try:
            return self.db.query(КлиентыM).filter(КлиентыM.клиент_id == клиент_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def delete_client(self, клиент_id: int) -> bool:
        try: 
            client_db = self.client_by_id(клиент_id)
            
            if client_db is None:
                return False

            self.db.delete(client_db)

            self.db.commit()
            
            return True

        except HTTPException:
            self.db.rollback()
            raise

