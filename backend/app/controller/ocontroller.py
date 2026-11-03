from typing import Dict, Any, Optional
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Coservice, require_roles

MAORoute = APIRouter(prefix="/operators", 
                   tags=["/operators"],
                   dependencies=[Depends(require_roles(["админ", "менеджер"]))]
                   )

AORoute = APIRouter(prefix="/operators", 
                   tags=["/operators"],
                   dependencies=[Depends(require_roles(["админ"]))]
                   )

@MAORoute.get("/operators")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении оператора: {str(e)}") 

@MAORoute.get("/operator_search")
def get_operators(оператор_id: Optional[int] = None, локации: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Sget_operator(оператор_id, локации)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении оператора: {str(e)}") 

@AORoute.post("/operator_create")
def create_operators(Odata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Screate_operator(Odata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании оператора {str(e)}")

@AORoute.put("/operator_update")
def update_operators(оператор_id: int, Oupdatedata: Dict[str, Any], db: Session = Depends(get_db) ):
    try:
        service = Coservice(db)
        return service.Supdate_operator(оператор_id, Oupdatedata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обнавлении оператора {str(e)}")

@AORoute.delete("/operator_delete")
def delete_operatora(оператор_id: int, db: Session = Depends(get_db)):
    try:
        service = Coservice(db)
        return service.Sdelete_operator(оператор_id)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении оператора {str(e)}")