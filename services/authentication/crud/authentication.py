from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from database.connection import get_db
from database.models.doctors import Doctor
from database.models.patients import Patient
from sqlalchemy.sql import exists,delete
from services.responses.errors import CustomError
from config import settings


# To get a string like this run:
# openssl rand -hex 32
# Its a seed to sign JWT tokens
SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm


# Token model
class Token(BaseModel):
    access_token: str
    token_type: str


# User Model
class User(BaseModel):
    username: str
    email: str
    id: int

# User model for password
class UserInDB(User):
    hashed_password: str

# Authentication class - Functions to authenticate users
class Authentication():

    # Hash password function
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

    # Verify if the password matches the hash in the database
    def verify_password(self,plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # Hash the password coming from the user
    def get_password_hash(self,password):
        return self.pwd_context.hash(password)

    
    # Return the user from the databasem- search by email
    def get_user(self, email: str, user_type: str):

        # Database connection 
        db = get_db()

        # Search user by email
        if user_type == 'patient':
            query = db.query(Patient).filter(Patient.email == email).first()

        elif user_type == 'doctor':
            query = db.query(Doctor).filter(Doctor.email == email).first()
        
        else:
            raise CustomError().error_400('User type not specified')

        # Closing the connection
        db.close()
        
        # if the user not exists, return None
        if query is None:
            return None

        # If the user exists, return the user
        return query
        
            

    # Authenticate the user in the database
    def authenticate_user(self, email: str, password: str, user_type: str):
        user = self.get_user(email, user_type)

        # Verify if the user exists
        if user is None:
            return False
        
        # If the user exists, verify if the password matches the hash in the database
        if not self.verify_password(password, user.password):
            return False
        
        # If the password matches, return the user
        return user

    # Generate a new JWT access token
    def create_access_token(self,data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_doctor(self, token:str = Depends(oauth2_scheme)):
        user = await self.get_current_user('doctor',token)
        return user

    async def get_patient(self,token: str = Depends(oauth2_scheme)):
        user =  await self.get_current_user('patient',token)
        return user

    # Verify if the JWT token is valid. If yes, get the user. If not, return exception
    async def get_current_user(self,user_type: str,token: str = Depends(oauth2_scheme)):
                

        # Decode the JWT token and verify if it's valid
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise CustomError().error_401(
                    'User not authenticated'
        )
        
        # If is not valid, return the credentials exception
        except JWTError:
            raise CustomError().error_401(
                'User not found'
        )
        
        # if is valid return the user
        user = self.get_user(email=username,user_type=user_type)
        if user is None:
            raise CustomError().error_401(
            'User not found'
        )
        return user

    

    # Check if the user has admin rights
    def is_doctor(self, user):
        '''Return True if the user is an admin'''
        
        comparision_user = Authentication().get_user(user.email,'doctor')

        if comparision_user:
            return True
        
        return False


class ResetPassword():

    # Reset password for the user
    def reset_password(self,email: str,password: str):
        '''
        email: str
        password: str

        Reset password for the user

        Example:

        '''

        db = get_db()

        # Get the user
        user = db.query(Lawyer).filter(Lawyer.email == email).first()

        # If the user exists, update the password
        if user is not None:
            user.password_digest = Authentication().get_password_hash(password)
            db.commit()
            db.close()
            return True
        
        else:
            db.close()
            return False

    # Get the id of the operator via email
    def get_id_operator_email(self,email: str):
        
        # Database connection
        db = get_db()
      
        query = db.query(Lawyer).filter(Lawyer.email == email).first()
        
        # Close the connection
        db.close()
        return query.id

