from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Clrepository

class Clvalidator(): 
    def __init__(self, repository: Clrepository):
        self.db = repository

    def validate_create_location(self, locationdata: Dict[str, Any]):
        """"Валидация перед создании локации"""

        required_fields = ["название", "адрес", "часы_работы"]

        for field in required_fields:

            if field not in locationdata or not locationdata[field]:
                
                raise HTTPException(status_code=400, detail=f"Поле '{field}' обязательно для заполнения")

        address = locationdata["адрес"]

        existing_address = self.db.location_by_address(address)

        if existing_address:

            raise HTTPException(status_code=400, detail=f"Адрес {str(address)} уже существует: ")


    def valifate_update_location(self, локация_id: int, locationupdatedata: Dict[str, Any]):
        """Валидация перед обновлении локации"""

        if "адрес" in locationupdatedata:

            new_address = locationupdatedata["адрес"]

            existing_address = self.db.location_by_address(new_address)

            if existing_address and existing_address.локация_id != локация_id:

                                raise HTTPException(status_code=400, detail=f"Локация с таким адресом '{new_address}' уже существует")