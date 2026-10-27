from typing import Dict, Any
from ..repositories import Crrepository
from ..validator import Crvalidator

class Crservice():

    def __init__(self, db):
        self.db = db
        self.repository = Crrepository(db)
        self.validator = Crvalidator(self.repository)

    def Screate_role(self, roledata: Dict) -> Dict[str, Any]:

            self.validator.validate_create_role(roledata)
            
            db_role_data = {
                "name": roledata["название_роли"],
                "description": roledata["описание"]
            }

            db_role = self.repository.create_role(db_role_data)

            return {
                "Message": "роль создана успешно",
                "role": {
                    "id": db_role.роль_id,
                    "name": db_role.название_роли,
                    "description": db_role.описание
                }
            }

    def Supdate_role(self, роль_id: int, updateroledata: dict) -> Dict[str, Any]:

        self.validator.validate_update_role(роль_id, updateroledata)

        db_role_update_data = {}

        if "название_роли" in updateroledata:
            db_role_update_data["name"] = updateroledata["название_роли"]
        if "описание" in updateroledata:
            db_role_update_data["description"] = updateroledata["описание"]

        db_role_update = self.repository.update_role(роль_id, db_role_update_data)

        return{
            "message": "Роль успешно обновлена",
            "role": {
                "id": db_role_update.роль_id,
                "name": db_role_update.название_роли,
                "description": db_role_update.описание
            }
        }

    def Sdelete_role(self, роль_id: int) -> Dict[str, Any]:
        self.repository.role_by_id(роль_id)

        self.repository.delete_role(роль_id)

        return {
            "message": "Роль успешно удалена"
        }