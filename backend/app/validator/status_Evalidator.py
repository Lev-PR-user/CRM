from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Cstatus_Erepository

class Cstatus_Evalidator():
    def __init__(self, repository: Cstatus_Erepository):
        self.repository = repository

    def validate_create_status(self, SEdata: Dict[str, Any]):
        """"Валидация перед создания статуса"""

        if "статус" not in SEdata or not SEdata["статус"]:

            raise HTTPException(status_code=400, detail="Название статуса обязательно для заполнения")

        name = SEdata["статус"]

        existing_status = self.repository.status_by_name(name)

        if existing_status: 

            raise HTTPException(status_code=400, detail=f"Статус с названием '{name}' уже существует")

    def validate_update_status(self, статус_оборудования_id: int, SEdataupdate: Dict[str, Any]): 
            """Валидация перед обновлением статуса""" 

            if "статус" in SEdataupdate: 

                new_name = SEdataupdate["статус"] 

                if not new_name: 

                    raise HTTPException(status_code=400, detail="Название статуса не может быть пустым") 
                
                existing_status = self.repository.status_by_name(new_name) 

                if existing_status and existing_status.статус_оборудования_id != статус_оборудования_id: 
                    
                    raise HTTPException(status_code=400, detail=f"Статус с названием '{new_name}' уже существует") 
        

