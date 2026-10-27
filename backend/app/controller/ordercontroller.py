from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Corderservice

ORDERoute = APIRouter(prefix="/orders", tags=["/orders"])

@ORDERoute.post("/order_create")
def create_order(orderdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Screate_order(orderdata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении заказа {str(e)}")

@ORDERoute.put("/order_update")
def update_order(заказ_id: int, orderupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Supdate_order(заказ_id, orderupdatedata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении заказа {str(e)}")

@ORDERoute.delete("/order_delete")
def delete_order(заказ_id: int, db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Sdelete_order(заказ_id)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении заказа {str(e)}")