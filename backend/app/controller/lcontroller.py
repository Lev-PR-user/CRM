from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Clservice, get_current_user

PLRoute = APIRouter(prefix="/plocations", tags=["/plocations"])

@PLRoute.get("/locations")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Clservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении локаций: {str(e)}")        

@PLRoute.get("/location_search")
def get_location(локация_id: Optional[int] = None, название: Optional[str] = None, адрес: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Clservice(db)
        return service.Sget_location(локация_id, название, адрес)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении локаций: {str(e)}")

LRoute = APIRouter(prefix="/locations", 
                   tags=["/locations"],
                   dependencies=[Depends(get_current_user)])

@LRoute.post("/location_create")
def create_location(locationdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Clservice(db)
        return service.Screate_location(locationdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании локации: {str(e)}")

@LRoute.put("/location_update")
def update_location(локация_id: int, locationupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Clservice(db)
        return service.Supdate_location(локация_id, locationupdatedata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении локации: {str(e)}")

@LRoute.delete("/location_delete")
def delete_location(локация_id: int, db: Session = Depends(get_db)):
    try:
        service = Clservice(db)
        return service.Sdelete_location(локация_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении локации: {str(e)}")