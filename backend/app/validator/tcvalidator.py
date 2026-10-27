from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Ctcrepository

class Сtcvalidator():
    def __init__(self, repository: Ctcrepository):
        self.repository = repository

    def validate_create_type_client(self, TCdata: Dict[str, Any]):
        """"Валидация перед создания типa"""

        if "тип" not in TCdata or not TCdata["тип"]:

            raise HTTPException(status_code=400, detail="Название типa обязательно для заполнения")

        type = TCdata["тип"]

        existing_type = self.repository.type_client_by_type(type)

        if existing_type: 

            raise HTTPException(status_code=400, detail=f"Тип с названием '{type}' уже существует")

    def validate_update_type_client(self, тип_клиента_id: int, TCupdatedata: Dict[str, Any]): 
            """Валидация перед обновлением типa""" 

            if "тип" in TCupdatedata: 

                new_type = TCupdatedata["тип"] 

                if not new_type: 

                    raise HTTPException(status_code=400, detail="Название типa не может быть пустым") 
                
                existing_type = self.repository.type_client_by_type(new_type) 

                if existing_type and existing_type.тип_клиента_id != тип_клиента_id: 
                    
                    raise HTTPException(status_code=400, detail=f"Типa с названием '{new_type}' уже существует") 
        

