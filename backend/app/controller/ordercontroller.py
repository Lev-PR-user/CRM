from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Corderservice, get_current_user, require_roles

ORDERoute = APIRouter(prefix="/orders", 
                      tags=["/orders"],
                      dependencies=[Depends(require_roles)])

@ORDERoute.get("/orders")
def get_all(пользователь_id: int = Depends(require_roles), db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Sget_order_for_user(пользователь_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении заказов: {str(e)}") 

@ORDERoute.get("/order_search")
def get_orders(заказ_id: int, пользователь_id: int = Depends(require_roles), db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Sget_by_id(заказ_id, пользователь_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении заказа: {str(e)}") 

@ORDERoute.post("/order_create")
def create_order(orderdata: Dict[str, Any], пользователь_id: int = Depends(require_roles), db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Screate_order(пользователь_id, orderdata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании заказа {str(e)}")

@ORDERoute.patch("/order_update")
def assing_resources(заказ_id: int, orderupdatedata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Sassign_resources(заказ_id, orderupdatedata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении заказа {str(e)}")

@ORDERoute.patch("/order_update_status")
def update_order(заказ_id: int, статус_заказа_id: int, пользователь_id: int = Depends(require_roles), db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return service.Supdate_status_order(заказ_id, статус_заказа_id, пользователь_id)
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