from typing import Dict, Any
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Ccservice, get_current_user

PCRoute = APIRouter(prefix="/pclients", tags=["/pclients"])

PCRoute.get("/clients")
def get_client(db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении клиента: {str(e)}")

CRoute = APIRouter(prefix="/clients", 
                   tags=["/clients"],
                   dependencies=[Depends(get_current_user)])

@CRoute.post("/client_create")
def create_client(clientdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.Screate_client(clientdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании клиента: {str(e)}")

@CRoute.put("/client_update")
def update_client(клиент_id: int, clientupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.Supdate_client(клиент_id, clientupdatedata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении клиента: {str(e)}")
    
@CRoute.delete("/client_delete")
def delete_client(клиент_id: int, db: Session = Depends(get_db)):
    try: 
        service = Ccservice(db)
        return service.Sdelete_client(клиент_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении клиента: {str(e)}")