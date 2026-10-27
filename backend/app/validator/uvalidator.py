from typing import Dict, Any
from fastapi import HTTPException
from ..repositories import CuRepository

class Cuvalidator: 
    def __init__(self, repository: CuRepository): 
        self.repository = repository 
        
    def validate_register(self, userdata: Dict[str, Any]): 
        """Валидация перед регистрацией нового пользователя""" 

        required_fields = ["фамилия", "имя", "пароль", "роль"] 

        for field in required_fields: 

            if field not in userdata or not userdata[field]: 

                raise HTTPException(status_code=400, detail=f"Поле '{field}' обязательно для заполнения") 
            
            email = userdata.get("почта") 

            number = userdata.get("номер")

            if email: 

                existing_user = self.repository.user_by_email(email) 

                if existing_user: 

                    raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует") 
                
            if number: 

                existing_user = self.repository.user_by_number(number) 

                if existing_user: 

                    raise HTTPException(status_code=400, detail="Пользователь с таким номером телефона уже существует") 
                    
    def validate_update(self, user_id: int, userdata: Dict[str, Any]): 
        """Валидация перед обновлением данных пользователя""" 

        email = userdata.get("почта") 

        number = userdata.get("номер") 

        if email: 

            existing_user = self.repository.user_by_email(email) 

            if existing_user and existing_user.пользователь_id != user_id: 

                raise HTTPException(status_code=400, detail="Эта почта уже занята другим пользователем") 
            
        if number: 

            existing_user = self.repository.user_by_number(number) 

            if existing_user and existing_user.пользователь_id != user_id: 
                
                raise HTTPException(status_code=400, detail="Этот номер телефона уже занят другим пользователем")