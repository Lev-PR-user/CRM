from typing import Dict, Any
from ..repositories import Corderrepository
# from ..validator import Cordervalidator

class Corderservice():
    def __init__(self, db):
        self.db = db
        self.repository = Corderrepository(db)
        # self.validator = Cordervalidator(self.repository)

    def Screate_order(self, orderdata: Dict[str, Any]) -> Dict[str, Any]:

        # self.validator.validate_create_order(orderdata)

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
            "order": {
                "id": db_order.заказ_id,
                "client": db_order.клиент,
                "service": db_order.услуги,
                "location": db_order.локации,
                "operator": db_order.оператор,
                "equipment": db_order.оборудование,
                "date_start": db_order.дата_начала,
                "date_end": db_order.дата_конца
            }
        }

    def Supdate_order(self, заказ_id: int, orderupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        # self.validator.validate_update_order(orderupdatedata)

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

        db_order_update = self.repository.update_order(заказ_id, db_order_update_data)

        return {
            "message": "Заказ обновлен",
            "order": {
                "id": db_order_update.заказ_id,
                "client": db_order_update.клиент,
                "service": db_order_update.услуги,
                "location": db_order_update.локации,
                "operator": db_order_update.оператор,
                "equipment": db_order_update.оборудование,
                "date_start": db_order_update.дата_начала,
                "date_end": db_order_update.дата_конца
            }
        }

    def Sdelete_order(self, заказ_id: int) -> Dict[str, Any]:

        self.repository.delete_order(заказ_id)

        return {
            "message": "Заказ удален"
        }