from typing import Dict, Any, Optional
from fastapi import HTTPException

class Cordervalidator():
    def create_order(self, orderdata: Dict[str, Any]):

        required_fields = ["услуги", "локации", "дата_начала", "дата_конца"]

        for field in required_fields:
            if field not in orderdata or not orderdata[field]:
                raise HTTPException(status_code=400, detail=f"Поля '{field}' обязательно для заполнения")

    def assign_resources(self, orderdata: Dict[str, Any]):

        required_fields = ["оператор", "оборудование"]

        for field in required_fields:
            if field not in orderdata or not orderdata[field]:
                raise HTTPException(status_code=400, detail=f"Поля '{field}' обязательно для заполнения")