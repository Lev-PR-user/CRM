from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from ..repositories import Corderrepository
from ..validator import Cordervalidator

class Corderservice():
    def __init__(self, db):
        self.db = db
        self.repository = Corderrepository(db)
        self.validator = Cordervalidator()

    @staticmethod
    def _public(db_order) -> Dict[str, Any]:
        return {
            "id": db_order.заказ_id,
            "client": db_order.клиент,
            "service": db_order.услуги,
            "location": db_order.локации,
            "operator": db_order.оператор,
            "equipment": db_order.оборудование,
            "date_start": db_order.дата_начала,
            "date_end": db_order.дата_конца
            }

    def Sget_order_for_user(self, пользователь_id: int) -> List[Dict[str, Any]]:
        role = self.repository.get_user_role(пользователь_id)

        if role in ("админ", "менеджер"):
            db_order = self.repository.get_all()
        elif role == "оператор":
            operator = self.repository.get_operator_by_user_id(пользователь_id)
            if not operator:
                return []
            db_order = self.repository.get_order_by_operator_id(operator.оператор_id)
        else:
            client = self.repository.get_client_by_user_id(пользователь_id)
            if not client:
                return []
            db_order = self.repository.get_order_by_client_id(client.клиент_id)
        
        return [self._public(o) for o in db_order]
    
    def Sget_by_id(self, заказ_id: int, пользователь_id: int):
        role = self.repository.get_user_role(пользователь_id)

        if role in ("админ", "менеджер"):
            db_order = self.repository.order_by_id(заказ_id)
        elif role == "оператор":
            operator = self.repository.get_operator_by_user_id(пользователь_id)
            if not operator:
                return []
            db_order = self.repository.get_order_by_id_and_operator_id(заказ_id, operator.оператор_id)
        else:
            client = self.repository.get_client_by_user_id(пользователь_id)
            if not client:
                return []
            db_order = self.repository.get_order_by_id_and_client_id(заказ_id, client.клиент_id)


        return self._public(db_order)

    def Screate_order(self, пользователь_id: int, orderdata: Dict[str, Any]) -> Dict[str, Any]:
        role = self.repository.get_client_by_user_id(пользователь_id)
        if not role:
            raise HTTPException(status_code=400, detail="У вас нет прав на создание заказа")

        self.validator.create_order(orderdata)    

        db_order_data = {
            "клиент": orderdata["client"],
            "услуги": orderdata["service"],
            "локации": orderdata["location"],
            "дата_начала":  orderdata["date_start"],
            "дата_конца":  orderdata["date_end"],
            "оператор": None,
            "оборудование": None,
            "статус": 1
            }
            
        self.repository.create_order(db_order_data)

        return {"message": "Заявка на заказ создана"}

    def Sassign_resources(self, заказ_id: int, orderdata: Dict[str, Any]) -> Dict[str, Any]:
        self.validator.assign_resources(orderdata)

        db_order = self.repository.update_order(заказ_id, {
            "оператор": orderdata["operator"],
            "оборудование": orderdata["equipment"],
            "статус": 2
        })

        return {
            "message": "Оператор и оборудование назначены",
            "order": self._public(db_order)
        }

    def Supdate_status_order(self, заказ_id: int, статус_заказа_id: int, пользователь_id: int) -> Dict[str, Any]:
        operator = self.repository.get_operator_by_user_id(пользователь_id)
        if not operator:
            raise HTTPException(status_code=403, detail="У вас нет профиля оператора")

        order = self.repository.get_order_by_id_and_operator_id(заказ_id, operator.оператор_id)
        if not order:
            raise HTTPException(status_code=403, detail="Вы не назначены на этот заказ")

        db_order = self.repository.update_order(заказ_id, {"статус": статус_заказа_id})

        return {
            "message": "Заказ обновлен",
            "order": self._public(db_order)
        }

    def Sdelete_order(self, заказ_id: int) -> Dict[str, Any]:

        self.repository.delete_order(заказ_id)

        return {
            "message": "Заказ удален"
        }