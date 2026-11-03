from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Ccservice, require_roles
# Добавить patch для типа клиента

MACRoute = APIRouter(
    prefix="/pclients", 
    tags=["/pclients"],
    dependencies=[Depends(require_roles(["админ", "менеджер"]))]
    )

ACRoute = APIRouter(
    prefix="/pclients", 
    tags=["/pclients"],
    dependencies=[Depends(require_roles(["админ"]))]
    )

@MACRoute.get("/clients")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении клиента: {str(e)}")

@MACRoute.get("/client_search")
def get_client(клиент_id: Optional[int] = None, имя: Optional[str] = None, db: Session = Depends(get_db)):
    try: 
        service = Ccservice(db)
        return service.Sget_client(клиент_id, имя)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении клиента: {str(e)}")

@ACRoute.post("/client_create")
def create_client(clientdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.Screate_client(clientdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании клиента: {str(e)}")

@MACRoute.put("/client_update")
def update_client(клиент_id: int, clientupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.Supdate_client(клиент_id, clientupdatedata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении клиента: {str(e)}")

@ACRoute.delete("/client_delete")
def delete_client(клиент_id: int, db: Session = Depends(get_db)):
    try: 
        service = Ccservice(db)
        return service.Sdelete_client(клиент_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении клиента: {str(e)}")