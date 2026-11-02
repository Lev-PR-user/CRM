from typing import Dict, Any, List, Optional
from ..repositories import Corderrepository

class Corderservice():
    def __init__(self, db):
        self.db = db
        self.repository = Corderrepository(db)

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

    def Sget_all(self, пользователь_id: int) -> List[Dict[str, Any]]:
        return [self._public(order) for order in self.repository.get_order_by_user_id(пользователь_id)]

    def Sget_by_id(self, заказ_id: Optional[int], пользователь_id: int):

        db_order = self.repository.order_by_id_and_user_id(заказ_id, пользователь_id)

        return self._public(db_order)

    def Screate_order(self, orderdata: Dict[str, Any]) -> Dict[str, Any]:

        db_order_data = {
            "клиент": orderdata["client"],
            "услуги": orderdata["service"],
            "локации": orderdata["location"],
            "оператор": orderdata["operator"],
            "оборудование": orderdata["equipment"]
            }

        db_order = self.repository.create_order(db_order_data)

        return {
            "message": "Заказ создан",
            "order": self._public(db_order)
        }

    def Supdate_order(self, заказ_id: int, orderupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        db_order_update_data = {}

        if "client" in orderupdatedata:
            db_order_update_data["клиент"] = orderupdatedata["client"]
        if "service" in orderupdatedata:
            db_order_update_data["услуги"] = orderupdatedata["service"]
        if "location" in orderupdatedata:
            db_order_update_data["локации"] = orderupdatedata["location"]
        if "operator" in orderupdatedata:
            db_order_update_data["оператор"] = orderupdatedata["operator"]
        if "equipment" in orderupdatedata:
            db_order_update_data["оборудование"] = orderupdatedata["equipment"]        

        db_order = self.repository.update_order(заказ_id, db_order_update_data)

        return {
            "message": "Заказ обновлен",
            "order": self._public(db_order)
        }

    def Sdelete_order(self, заказ_id: int) -> Dict[str, Any]:

        self.repository.delete_order(заказ_id)

        return {
            "message": "Заказ удален"
        }