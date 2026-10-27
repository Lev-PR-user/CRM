from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Corepository

class Covalidator():
    def __init__(self, repository: Corepository):
        self.db = repository

    def validate_create_operators(self, Odata: Dict[str, Any]):
        """Валидация перед созданием оператора"""

        required_fields = ["пользователь", "локации", "график"]

        for field in required_fields:

            if field not in Odata or not Odata[field]:
                
                raise HTTPException(status_code=400, detail=f"Поля '{str(field)}' обязательны для заполнения")


    def validate_update_operators(self, Oupdatedata: Dict[str, Any]):
        """Валидация перед обновлением оператора"""

        required_fields = ["пользователь", "локации", "график"]

        for field in required_fields:
            
            if field not in Oupdatedata or not Oupdatedata[field]:
                
                raise HTTPException(status_code=400, detail=f"Поля '{str(field)}' обязательны для заполнения")
        
