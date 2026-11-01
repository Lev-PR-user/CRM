from typing import Dict, Any, Optional
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Csservice, get_current_user

PSRoute = APIRouter(prefix="/pservices", tags=["services"])

@PSRoute.get("/services")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Csservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении услуг: {str(e)}")

@PSRoute.get("/service_search")
def get_service( услуга_id: Optional[int] = None, услуга: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Csservice(db)
        return service.Sget_service(услуга_id, услуга)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении услуг: {str(e)}")

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
def update_service(serviceupdatedata: Dict[str, Any], услуга_id: Optional[int] = None, услуга: Optional[str] = None, db: Session = Depends(get_db)):
    try: 
        service = Csservice(db)
        return service.Supdate_service(serviceupdatedata, услуга_id, услуга)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении услуги: {str(e)}")

@SRoute.delete("/service_delete")
def delete_service(услуга_id: Optional[int] = None, услуга: Optional[str] = None, db: Session = Depends(get_db)):
    try: 
        service = Csservice(db)
        return service.Sdelete_service(услуга_id, услуга)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении услуги: {str(e)}")
