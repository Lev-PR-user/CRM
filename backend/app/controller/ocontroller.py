from typing import Dict, Any, Optional
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Coservice

ORoute = APIRouter(prefix="/operators", tags=["/operators"])

@ORoute.post("/operators_create")
def create_operators(Odata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Screate_operator(Odata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании оператора {str(e)}")

@ORoute.put("/operators_update")
def update_operators(оперетор_id: int, Oupdatedata: Dict[str, Any], db: Session = Depends(get_db) ):
    try:
        service = Coservice(db)
        return service.Supdate_operator(оперетор_id, Oupdatedata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обнавлении оператора {str(e)}")

@ORoute.delete("/operators_delete")
def delete_operatora(оперетор_id: int, db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Sdelete_operator(оперетор_id)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении оператора {str(e)}")