from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from database.connection import get_db
from database.models.doctors import Doctor
from database.models.patients import Patient
from database.basic import BasicCrud
from sqlalchemy.sql import exists,delete
from services.responses.errors import CustomError
from config import settings

class SignUpManager(BasicCrud):
    # Choose the type of user
    def __init__(self, user_type: str):
        
        if user_type == 'patient':
            super().__init__(Patient)
        
        elif user_type == 'doctor':
            super().__init__(Doctor)
        
        else:
            raise CustomError().error_400(
                'User type not selected'
            )
