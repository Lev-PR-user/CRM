# создание токена, хэш паролей
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

SECURITE_KEY=os.getenv("SECURITE_KEY")


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
