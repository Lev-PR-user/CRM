from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Csrepository

class Csvalidator():
    def __init__(self, repository: Csrepository):
        self.repository = repository

    def validate_create_service(self, servicedata: Dict[str, Any]):
        """"Валидация создания услуги"""

        if "услуга" not in servicedata or not servicedata["услуга"]:

            raise HTTPException(status_code=400, detail="Название услуги обязательно для заполнения")

        name = servicedata["услуга"]

        existing_status = self.repository.service_by_name(name)

        if existing_status: 

            raise HTTPException(status_code=400, detail=f"Нслуга с названием '{name}' уже существует")

    def validate_update_status(self, услуга_id: int, serviceupdatedata: Dict[str, Any]): 
                """Валидация перед обновлением услуги""" 

                if "услуга" in serviceupdatedata: 

                    new_name = serviceupdatedata["услуга"] 

                    if not new_name: 

                        raise HTTPException(status_code=400, detail="Название услуги не может быть пустым") 
                    
                    existing_status = self.repository.service_by_name(new_name) 

                    if existing_status and existing_status.услуга_id != услуга_id: 
                        
                        raise HTTPException(status_code=400, detail=f"Услуга с названием '{new_name}' уже существует") 