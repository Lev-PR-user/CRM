from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Crservice, get_current_user

RRoute = APIRouter(prefix="/roles", 
                   tags=["roles"],
                   dependencies=[Depends(get_current_user)])

@RRoute.get("/roles")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Crservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении ролей: {str(e)}") 

@RRoute.get("/role_search")
def get_roles(роль_id: Optional[int] = None, название_роли: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Crservice(db)
        return service.Sget_role(роль_id, название_роли)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении роли: {str(e)}") 

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
def update_role(updateroledata: Dict[str, Any], роль_id: Optional[int] = None, название_роли: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Crservice(db)
        return service.Supdate_role(updateroledata, роль_id, название_роли)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении роли {str(e)}")

@RRoute.delete("/delete")
def delete_role(роль_id: Optional[int] = None, название_роли: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Crservice(db)
        return service.Sdelete_role(роль_id, название_роли)
    except HTTPException:
        raise 
    except Exception as e:
        HTTPException(status_code=500, detail=f"Ошибка при удалении роли: {str(e)}")
