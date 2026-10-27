from typing import Dict, Any
from fastapi import HTTPException
from ..validator import Cuvalidator
from ..repositories import CuRepository
from .authservice import createtoken, password_hash, verify_password

class Cuservice:
    def __init__(self, db):
        self.db = db
        self.repository = CuRepository(db)
        self.validator = Cuvalidator(self.repository)

    def Sregister(self, userdata: Dict) -> Dict[str, Any]:

        self.validator.validate_register(userdata)  

        h_password = password_hash(userdata["пароль"])

        db_user_data = {
            "secondname": userdata["фамилия"],
            "name": userdata["имя"],
            "password": h_password,
            "middlename": userdata.get("отчество"),
            "name_organition": userdata.get("название_организации"),
            "email": userdata.get("почта"),
            "number": userdata.get("номер"),
            "role": userdata["роль"]
        }

        db_user = self.repository.create_user(db_user_data)

        token = createtoken(data={"sub": str(db_user.пользователь_id)})

        return {
            "message": "Пользователь создан",
            "user": {
                "id": db_user.пользователь_id,
                "secondname": db_user.фамилия,
                "name": db_user.имя,
                "middlename": db_user.отчество,
                "name_organition": db_user.название_организации,
                "email": db_user.почта,
                "number": db_user.номер,
                "role": db_user.роль
            },
            "token": token, #токен
            "token_type": "bearer"
        }

    def Slogin(self, logindata: Dict) -> Dict[str, Any]:
            
        email = logindata.get("почта")
        plan_password = logindata.get("пароль")
        number = logindata.get("номер")

        if email:
            db_user = self.repository.user_by_email(email)
        elif number:
            db_user = self.repository.user_by_number(number)
        else:
            raise HTTPException(status_code=400, detail="Укажите почту или пароль")

        if db_user is None:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        
        if not verify_password(plan_password, db_user.пароль):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        token = createtoken(data={"sub": str(db_user.пользователь_id)})

        return {
            "message": "Авторизация прошла успешно",
             "user": {
                 "id": db_user.пользователь_id,
                 "secondname": db_user.фамилия,
                 "name": db_user.имя,
                 "middlename": db_user.отчество,
                 "name_organition": db_user.название_организации,
                 "email": db_user.почта,
                 "number": db_user.номер,
                 "role": db_user.роль
             },
             "token": token, #токен
             "token_type": "bearer"
        }


    def Supdate_user(self, пользователь_id: int, updateuserdata: Dict) -> Dict[str, Any]:

        self.validator.validate_update(пользователь_id, updateuserdata)

        db_user_update_data = {}
        
        if "фамилия" in updateuserdata:
            db_user_update_data["secondname"] = updateuserdata["фамилия"]
        if "имя" in updateuserdata:
            db_user_update_data["name"] = updateuserdata["имя"]
        if "пароль" in updateuserdata:
            db_user_update_data["password"] = password_hash(updateuserdata["пароль"])
        if "отчество" in updateuserdata:
            db_user_update_data["middlename"] = updateuserdata["отчество"]
        if "название_организации" in updateuserdata:
            db_user_update_data["name_organition"] = updateuserdata["название_организации"]
        if "почта" in updateuserdata:
            db_user_update_data["email"] = updateuserdata["почта"]
        if "номер" in updateuserdata:
            db_user_update_data["number"] = updateuserdata["номер"]

        db_user_update = self.repository.update_user(пользователь_id, db_user_update_data)

        return {
            "message": "Данные успешно обновлены",
            "user": {
                "secondname": db_user_update.фамилия,
                "name": db_user_update.имя,
                "middlename": db_user_update.отчество,
                "name_organition": db_user_update.название_организации,
                "email": db_user_update.почта,
                "number": db_user_update.номер
            }
        }

    def Sdelete_user(self, пользователь_id: int) -> Dict[str, Any]:
        self.repository.user_by_id(пользователь_id)

        self.repository.delete_user(пользователь_id)  

        return{
            "message": "Пользователь удален"
        }      