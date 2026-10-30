from typing import Dict, Any
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Csservice, get_current_user

SRoute = APIRouter(prefix="/services", 
                   tags=["/services"],
                   dependencies=[Depends(get_current_user)])

@SRoute.post("/service_create")
def create_service(servicedata: Dict[str, Any], db: Session = Depends(get_db)):
    try: 
        service = Csservice(db)
        return service.Screate_service(servicedata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании услуги: {str(e)}")

@SRoute.put("/service_update")
def update_service(услуга_id: int, serviceupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try: 
        service = Csservice(db)
        return service.Supdate_service(услуга_id, serviceupdatedata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении услуги: {str(e)}")

@SRoute.delete("/service_delete")
def delete_service(услуга_id: int, db: Session = Depends(get_db)):
    try: 
        service = Csservice(db)
        return service.Sdelete_service(услуга_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении услуги: {str(e)}")
