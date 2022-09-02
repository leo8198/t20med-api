from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from services.authentication.connectors.my_email import EmailAPI
from services.authentication.crud.authentication import Authentication, User, ResetPassword
from services.authentication.schemas.reset_password import UserReset
from services.responses.errors import CustomError
from services.responses.responses import CustomResponse

# Endpoint to handle the authentication functions
router = APIRouter(
    prefix='/api/v1'
)

# JWT expire time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 8*60


# Endpoint to send the reset password email
@router.get("/reset-password/{email}")
async def reset_password_email(email: str):
    
    # Create a token
    access_token_expires = timedelta(minutes=60)
    access_token = Authentication().create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )


    # Send email with the token
    EmailAPI().send_first_password_email(email,access_token)

    return CustomResponse().success_without_data()

# Endpoint to update the operator password
@router.put("/reset-password")
async def reset_password(
    user_data: UserReset,
    current_user: User = Depends(Authentication().get_current_user)):

    # Get the user from the database
    if current_user:
        
        # Update the user password
        if ResetPassword().reset_password(current_user.email,user_data.password):
            
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
