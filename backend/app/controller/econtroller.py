from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..services import Ceservice, get_current_user
from ..db import get_db

ERoute = APIRouter(prefix="/equipment", 
                   tags=["/equipment"],
                   dependencies=[Depends(get_current_user)])

@ERoute.post("/create_equipment")
def create_equipment(equipmentdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ceservice(db)
        return service.Screate_equipment(equipmentdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании оборудования: {str(e)}")

@ERoute.put("/update_equipment")
def update_equipment(оборудование_id: int, equipmentupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ceservice(db)
        return service.Supdate_equipment(equipmentupdatedata, оборудование_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении оборудования: {str(e)}")

@ERoute.delete("/delete_equipment")
def delete_equipment(оборудование_id: int, db: Session = Depends(get_db)):
    try:
        service = Ceservice(db)
        return service.Sdelete_equipment(оборудование_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления оборудования: {str(e)}")