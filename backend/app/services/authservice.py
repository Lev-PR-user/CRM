# создание токена, хэш паролей
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import bcrypt
from ..db import get_db
from ..models import ПользователиM

load_dotenv()

SECURITE_KEY=os.getenv("SECURITE_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/pusers/login")

ALGORITM='HS256'
ACCESS_TOKEN_EXIRE_MINUTES=30

def createtoken(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    
    to_encode = data.copy()

    if expires_delta:

        expire = datetime.now(timezone.utc) + expires_delta

    else:

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECURITE_KEY, algorithm=ALGORITM)

    return encoded_jwt

def password_hash(пароль: str) -> str:
    password_bytes = пароль.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plan_password: str, пароль: str ) -> bool:
    try:
        return bcrypt.checkpw(
            plan_password.encode("utf-8"),
            пароль.encode("utf-8")
        )
    except ValueError:
        return False


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
        pyload = jwt.decode(token, SECURITE_KEY, algorithms=[ALGORITM])
        user_id = pyload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return int(user_id)

def require_roles(allowed_roles: List[str]):
    def role_checker(пользователь_id: int = Depends(get_current_user), db: Session = Depends(get_db)) -> int:

        user = db.query(ПользователиM).filter(ПользователиM.пользователь_id == пользователь_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")

        if not user.роли:
            raise HTTPException(status_code=403, detail="У вас не назначена роль")

        if user.роли.название_роли not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"Доступ запрещен. Требуется роль: {', '.join(allowed_roles)}")

        return пользователь_id
    return role_checker