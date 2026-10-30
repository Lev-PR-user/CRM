from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from ..db import get_db
from ..services import Ctcservice, get_current_user

TCRoute = APIRouter(prefix="/type_clients", 
                    tags=["/type_clients"],
                    dependencies=[Depends(get_current_user)])

@TCRoute.get("/type_clients")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Ctcservice(db)
        return service.get_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении типа коиента: {str(e)}")

@TCRoute.get("/type_client_search")
def get_type_clients(тип: Optional[str], тип_клиента_id: Optional[int], db: Session = Depends(get_db)):
    try:
        service = Ctcservice(db)
        return service.get_type_client(тип, тип_клиента_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении типа клиента: {str(e)}")

@TCRoute.post("/type_client_create")
def create_type_client(TCdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ctcservice(db)
        return service.Screate_type_client(TCdata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании типа клиента: {str(e)}")

@TCRoute.put("/type_client_update")
def update_type_client(TCupdatedata: Dict[str, Any], тип: Optional[str], тип_клиента_id: Optional[int], db: Session = Depends(get_db)):
    try:
        service = Ctcservice(db)
        return service.Supdate_type_client(тип, тип_клиента_id, TCupdatedata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении типа клиента: {str(e)}")

@TCRoute.delete("/type_client_delete")
def delete_type_client(тип: Optional[str] = None, тип_клиента_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        service = Ctcservice(db)
        return service.Sdelete_type_client( тип_клиента_id, тип)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении типа клиента {str(e)}")
