from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Corderservice, get_current_user

ORDERoute = APIRouter(prefix="/orders", 
                      tags=["/orders"],
                      dependencies=[Depends(get_current_user)])

@ORDERoute.get("/orders")
def get_all(пользователь_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении заказов: {str(e)}") 

@ORDERoute.get("/order_search")
def get_orders(заказ_id: Optional[int], пользователь_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        service = Corderservice(db)
        return 
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении заказа: {str(e)}") 

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