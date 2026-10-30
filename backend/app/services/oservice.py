from typing import Dict, Any
from ..repositories import Corepository
from ..validator import Covalidator

class Coservice():
    def __init__(self, db):
        self.db = db
        self.repository = Corepository(db)
        self.validator = Covalidator(self.repository)

    @staticmethod
    def _public(db_operator) -> Dict[str, Any]:
        return {
            "id": db_operator.оператор_id,
            "user": db_operator.пользователь,
            "locationn": db_operator.локации,
            "shedule": db_operator.график
        }

    def Screate_operator(self, Odata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_create_operators(Odata)

        db_operator_data = {
            "user": Odata["пользователь"],
            "location": Odata["локации"],
            "schedule": Odata["график"]
        }

        db_operator = self.repository.create_operator(db_operator_data)

        return {
            "message": "Оператор успешно создан",
            "operator": self._public(db_operator)
        }

    def Supdate_operator(self, оператор_id: int, Oupdatedata: Dict[str, Any]) -> Dict[str, Any]:

        self.validator.validate_update_operators(Oupdatedata)

        db_operator_update_data = {}

        if "пользователь" in Oupdatedata:
            db_operator_update_data["user"] = Oupdatedata["пользователь"]
        if "локации" in Oupdatedata:
            db_operator_update_data["location"] = Oupdatedata["локации"]
        if "график" in Oupdatedata:
            db_operator_update_data["shedule"] = Oupdatedata["график"]

        db_operator = self.repository.update_operator(оператор_id, db_operator_update_data)

        return {
            "message": "Оператор успешно обновлен",
            "operator": self._public(db_operator)
        }

    def Sdelete_operator(self, оператор_id: int) -> Dict[str, Any]:

        self.repository.delete_operator(оператор_id)

        return {
            "message": "Оператор удален"
        }