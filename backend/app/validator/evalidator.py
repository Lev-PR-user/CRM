from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Cerepository

class Cevalidator():
    def __init__(self, repository: Cerepository):
        self.repository = repository

    def validate_create_equipment(self, equipmentdata: Dict[str, Any]): 
        """Валидация перед созданию оборудрвания""" 
        
        required_fields = ["модель", "серия", "статус", "расположение"] 

        for field in required_fields: 

            if field not in equipmentdata or not equipmentdata[field]: 

                raise HTTPException(status_code=400, detail=f"Поле '{field}' обязательно для заполнения")