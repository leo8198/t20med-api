from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from services.authentication.crud.authentication import Authentication, User, ResetPassword
from services.responses.errors import CustomError
from services.responses.responses import CustomResponse

# Endpoint to handle the authentication functions
router = APIRouter(
    prefix='/api/v1'
)

# JWT expire time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 14*60

# Endpoint to create the access token
@router.post("/login")
async def login_for_access_token(
    user_type: str,
    form_data: OAuth2PasswordRequestForm = Depends()):
    
    
    # Authenticate the user in the database
    user = Authentication().authenticate_user(form_data.username, form_data.password, user_type)
    

    # If the user is not found, return the credentials exception
    if not user:
        raise CustomError().error_401(
            'Wrong email or password'
        )

    # If the user is found, generate the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Authentication().create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )


    # Return the access token
    return {"detail":{"status":"ok","status_code":0},
            "access_token": access_token,
            "token_type": "bearer",
            }

