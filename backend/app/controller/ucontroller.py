from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services import Cuservice, get_current_user
from ..db import get_db

URoute = APIRouter(prefix="/pusers", tags=["pusers"])


@URoute.post("/registers")
def register(userdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cuservice(db)
        return service.Sregister(userdata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка регистрации: {str(e)}")

@URoute.post("/login")
def login(logindata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cuservice(db)
        return service.Slogin(logindata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка входа: {str(e)}")


DURoute = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)])

@DURoute.get("/profile")
def profle(пользователь_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try: 
        service = Cuservice(db)
        return service.Sprofile(пользователь_id)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных профиля: {str(e)}")

@DURoute.put("/update")
def update_user(updateuserdata: Dict, пользователь_id: int = Depends(get_current_user),  db: Session = Depends(get_db)):
    try:
        service = Cuservice(db)
        return service.Supdate_user(пользователь_id, updateuserdata)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления данных: {str(e)}")
    
@DURoute.delete("/delete")
def delete_user(пользователь_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        service = Cuservice(db)
        return service.Sdelete_user(пользователь_id)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления пользователя: {str(e)}")