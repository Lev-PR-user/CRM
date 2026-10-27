from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import Crrepository

class Crvalidator: 
    def __init__(self, repository: Crrepository): 
        self.repository = repository 
        
    def validate_create_role(self, roledata: Dict[str, Any]): 
        """Валидация перед созданием роли""" 

        if "название_роли" not in roledata or not roledata["название_роли"]: 

            raise HTTPException(status_code=400, detail="Название роли обязательно для заполнения")
        
        name = roledata["название_роли"] 

        existing_role = self.repository.role_by_name(name) 

        if existing_role: 

            raise HTTPException(status_code=400, detail=f"Роль с названием '{name}' уже существует") 
        
    def validate_update_role(self, роль_id: int, updateroledata: Dict[str, Any]): 
        """Валидация перед обновлением роли""" 

        if "название_роли" in updateroledata: 

            new_name = updateroledata["название_роли"] 

            if not new_name: 

                raise HTTPException(status_code=400, detail="Название роли не может быть пустым") 
            
            existing_role = self.repository.role_by_name(new_name) 

            if existing_role and existing_role.роль_id != роль_id: 
                
                raise HTTPException(status_code=400, detail=f"Роль с названием '{new_name}' уже существует")