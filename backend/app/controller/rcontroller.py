from typing import Dict, Any 
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Crservice, get_current_user

RRoute = APIRouter(prefix="/roles", 
                   tags=["roles"],
                   dependencies=[Depends(get_current_user)])

@RRoute.post("/createrole")
def create_role(roledata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Crservice(db)
        return service.Screate_role(roledata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании роли {str(e)}")

@RRoute.put("/update")
def update_role(роль_id: int, updateroledata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Crservice(db)
        return service.Supdate_role(роль_id, updateroledata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении роли {str(e)}")

@RRoute.delete("/delete")
def delete_role( роль_id: int, db: Session = Depends(get_db)):
    try:
        service = Crservice(db)
        return service.Sdelete_role(роль_id)
    except HTTPException:
        raise 
    except Exception as e:
        HTTPException(status_code=500, detail=f"Ошибка при удалении роли: {str(e)}")
