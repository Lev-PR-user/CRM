from typing import Dict, Any, Optional
from fastapi import HTTPException
from ..repositories import Crrepository
from ..validator import Crvalidator

class Crservice():

    def __init__(self, db):
        self.db = db
        self.repository = Crrepository(db)
        self.validator = Crvalidator(self.repository)

    @staticmethod
    def _public(db_role) -> Dict[str, Any]:
        return {
            "id": db_role.роль_id,
            "name": db_role.название_роли,
            "description": db_role.описание
            }
    
    def Sget_all(self):
        return [self._public(r) for r in self.repository.get_all()]

    def Sget_role(self, роль_id: Optional[int], название_роли: Optional[str]):

        if роль_id:
            db_role = self.repository.role_by_id(роль_id)
        elif название_роли:
            db_role = self.repository.role_by_name(название_роли)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска") 

        if db_role is None:
            raise HTTPException(status_code=400, detail="Такой роли нет") 

        return self._public(db_role)
 

    def Screate_role(self, roledata: Dict) -> Dict[str, Any]:

            self.validator.validate_create_role(roledata)
            
            db_role_data = {
                "name": roledata["название_роли"],
                "description": roledata["описание"]
            }

            db_role = self.repository.create_role(db_role_data)

            return {
                "Message": "роль создана успешно",
                "role": self._public(db_role)
            }

    def Supdate_role(self, роль_id: Optional[int], название_роли: Optional[str], updateroledata: dict) -> Dict[str, Any]:

        self.validator.validate_update_role(роль_id, updateroledata)

        db_role_update_data = {}

        if "название_роли" in updateroledata:
            db_role_update_data["name"] = updateroledata["название_роли"]
        if "описание" in updateroledata:
            db_role_update_data["description"] = updateroledata["описание"]

        db_role = self.repository.update_role(роль_id, название_роли, db_role_update_data)

        return{
            "message": "Роль успешно обновлена",
            "role": self._public(db_role)
        }

    def Sdelete_role(self, роль_id: int) -> Dict[str, Any]:
        self.repository.role_by_id(роль_id)

        self.repository.delete_role(роль_id)

        return {
            "message": "Роль успешно удалена"
        }