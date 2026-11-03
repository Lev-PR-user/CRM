from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import ЗаказыM, КлиентыM, ОператорыM

class Corderrepository():
    def __init__(self, db: Session):
        self.db = db        

    def get_operator_by_user_id(self, пользователь_id: int) -> Optional[ОператорыM]:
        try:
            return self.db.execute(select(ОператорыM).where(ОператорыM.пользователь == пользователь_id)).scalar_one_or_none()
        except HTTPException:
            self.db.rollback()
            raise

    def get_client_by_user_id(self, пользователь_id: int) -> Optional[КлиентыM]:
        try:
            return self.db.execute(select(КлиентыM).where(КлиентыM.пользователь == пользователь_id)).scalar_one_or_none()
        except HTTPException:
            self.db.rollback()
            raise

    def get_order_by_user_id(self, пользователь_id: int) -> List[ЗаказыM]:
        try:
            return self.db.query(ЗаказыM).join(
                КлиентыM, ЗаказыM.клиент == КлиентыM.клиент_id ).filter(
                    КлиентыM.пользователь == пользователь_id
                ).all()
        except HTTPException:
            self.db.rollback()
            raise

    def get_order_by_id_and_user_id(self, заказ_id: int, пользователь_id: int) -> Optional[ЗаказыM]:
        try:
            return self.db.query(ЗаказыM).join(
                КлиентыM, ЗаказыM.клиент == КлиентыM.клиент_id ).filter(
                    ЗаказыM.заказ_id == заказ_id,
                    КлиентыM.пользователь == пользователь_id
                ).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_order_by_operator_id(self, оператор_id: int) -> List[ЗаказыM]:
        try:
            return list(self.db.execute(select(ЗаказыM).where(ЗаказыM.оператор == оператор_id)).scalars().all())
        except HTTPException:
            self.db.rollback()
            raise

    def get_order_by_id_and_operator_id(self, оператор_id: int,  заказ_id: int) -> Optional[ЗаказыM]:
        try: 
            return self.db.execute(select(ЗаказыM).where(ЗаказыM.заказ_id == заказ_id,
                                                         ЗаказыM.оператор == оператор_id)).scalar_one_or_none()
        except HTTPException:
            self.db.rollback()
            raise

    def get_all(self) -> List[ЗаказыM]:
        try: 
            return self.db.query(ЗаказыM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def create_order(self, orderdata: Dict[str, Any]) -> ЗаказыM:
        try:

            order_db = ЗаказыM(
                клиент=orderdata["client"],
                услуги=orderdata["service"],
                локации=orderdata["location"],
                оператор=orderdata["operator"],
                оборудование=orderdata["equipment"]
            )

            self.db.add(order_db)

            self.db.commit()

            self.db.refresh(order_db)

            return order_db
        
        except HTTPException:
            self.db.rollback()
            raise


    def update_order(self, заказ_id: int, orderupdatedata: Dict[str, Any]) -> ЗаказыM:
        try:    

            order_update_db = self.order_by_id(заказ_id)

            if order_update_db is None:
                raise HTTPException(status_code=500, detail="Такого заказа нет")

            if "client" in orderupdatedata:
                order_update_db.клиент = orderupdatedata["client"]
            if "service" in orderupdatedata:
                order_update_db.услуги = orderupdatedata["service"]
            if "location" in orderupdatedata:
                order_update_db.локации = orderupdatedata["location"]
            if "operator" in orderupdatedata:
                order_update_db.оператор = orderupdatedata["operator"]
            if "equipment" in orderupdatedata:
                order_update_db.оборудование = orderupdatedata["equipment"]

            self.db.commit()

            self.db.refresh(order_update_db)

            return order_update_db

        except HTTPException:
            self.db.rollback()
            raise

    def order_by_id(self, заказ_id: int) -> Optional[ЗаказыM]:
        try: 
            return self.db.query(ЗаказыM).filter(ЗаказыM.заказ_id == заказ_id).first()
        except Exception as e:

            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def delete_order(self, заказ_id: int) -> bool:
        try: 
            order_db = self.order_by_id(заказ_id)

            if order_db is None:
                return False

            self.db.commit()

            self.db.delete(order_db)

            return True

        except HTTPException:
            self.db.rollback()
            raise
