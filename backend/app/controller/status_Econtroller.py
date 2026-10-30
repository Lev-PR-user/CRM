from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Cstatus_Eservice, get_current_user

SERoute = APIRouter(prefix="/status_equipments", 
                    tags=["/status_equipments"],
                    dependencies=[Depends(get_current_user)])

@SERoute.get("/status_equipments")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Cstatus_Eservice(db)
        return service.get_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статуса оборудования: {str(e)}")

@SERoute.get("/status_equipment_search")
def get_status_equipments(статус_уведомления_id: Optional[int], статус: Optional[str], db: Session = Depends(get_db)):
    try:
        service = Cstatus_Eservice(db)
        return service.get_status_equipment(статус_уведомления_id, статус)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статуса оборудования: {str(e)}")

@SERoute.post("/status_equipment_create")
def create_status_equipment(SEdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cstatus_Eservice(db)
        return service.Screate_status_equipment(SEdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании статуса оборудования: {str(e)}")

@SERoute.put("/status_equipment_update")
def update_status_equipment(статус_оборудования_id: int, SEdataupdate: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cstatus_Eservice(db)
        return service.Supdate_status_equipment(SEdataupdate, статус_оборудования_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении статуса оборудования: {str(e)}")

@SERoute.delete("/status_equipment_delete")
def delete_status_equipment(статус_оборудования_id: int, db: Session = Depends(get_db)):
    try:
        service = Cstatus_Eservice(db)
        return service.Sdelete_status_equipment(статус_оборудования_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении статуса оборудования: {str(e)}")