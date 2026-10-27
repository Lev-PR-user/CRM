from typing import Dict, Any
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Ccservice

CRoute = APIRouter(prefix="/clients", tags=["/clients"])

@CRoute.post("/client_create")
def create_client(clientdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.create_client(clientdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании клиента: {str(e)}")

@CRoute.put("/client_update")
def update_client(клиент_id: int, clientupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccservice(db)
        return service.update_client(клиент_id, clientupdatedata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении клиента: {str(e)}")
    
@CRoute.delete("/client_delete")
def delete_client(клиент_id: int, db: Session = Depends(get_db)):
    try: 
        service = Ccservice(db)
        return service.delete_client(клиент_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении клиента: {str(e)}")