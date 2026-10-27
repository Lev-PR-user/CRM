from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Ccrepository

class Ccvalidator():
    def __init__(self, repository: Ccrepository):
        self.repository = repository

    def validate_create_client(self, clientdata: Dict[str, Any]):
        """Валидация перед созданием клиента"""

        required_fields = ["имя", "тип", "контакты"]

        for field in required_fields:

            if field not in clientdata or not clientdata["field"]:

                raise HTTPException(status_code=400, detail=f"Поле '{field}' обязательно для заполнения")

    def validate_update_client(self, clientupdatedata: Dict[str, Any]):
        """Валидация перед обновлением клиента"""

        required_fields = ["имя", "тип", "контакты"]

        for field in required_fields:

            if field not in clientupdatedata or not clientupdatedata["field"]:
                
                raise HTTPException(status_code=400, detail=f"Поле '{field}' обязательно для заполнения")