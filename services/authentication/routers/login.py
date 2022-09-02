from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from services.authentication.crud.authentication import Authentication, User, ResetPassword
#from app.schemas.user import UserReset
#from app.external.apis.my_email import EmailAPI
from services.responses.errors import CustomError
from services.responses.responses import CustomResponse

# Endpoint to handle the authentication functions
router = APIRouter(
    prefix='/api/v1'
)

# JWT expire time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 8*60

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

# Endpoint to send the reset password email
@router.get("/reset-password/{email}")
async def reset_password_email(email: str):
    
    # Create a token
    access_token_expires = timedelta(minutes=60)
    access_token = Authentication().create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )


    # Send email with the token
   # EmailAPI().send_first_password_email(email,access_token)

    return CustomResponse().success_without_data()

# Endpoint to update the operator password
@router.put("/reset-password")
async def reset_password(background_tasks: BackgroundTasks,current_user: User = Depends(Authentication().get_current_user)):

    # Get the user from the database
    if current_user:
        
        # Update the user password
        if True:#ResetPassword().reset_password(current_user.email,user_data.password):
            
            return CustomResponse().success_without_data()

        # Passoword update failed        
        else:
            
            return CustomError().error_500(
                'Error when updating the password'
            )

    # Invalid bearer token
    else:
        raise CustomError().error_401(
            'Invalid Bearer Token'
        )
