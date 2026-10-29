from typing import Dict, Any, Optional
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Coservice

ORoute = APIRouter(prefix="/operators", tags=["/operators"])

@ORoute.post("/operator_create")
def create_operators(Odata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Screate_operator(Odata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании оператора {str(e)}")

@ORoute.put("/operator_update")
def update_operators(оператор_id: int, Oupdatedata: Dict[str, Any], db: Session = Depends(get_db) ):
    try:
        service = Coservice(db)
        return service.Supdate_operator(оператор_id, Oupdatedata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обнавлении оператора {str(e)}")

@ORoute.delete("/operator_delete")
def delete_operatora(оператор_id: int, db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Sdelete_operator(оператор_id)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении оператора {str(e)}")