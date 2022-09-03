from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from services.authentication.crud.authentication import Authentication
from services.authentication.crud.signup import SignUpManager
from services.authentication.schemas.signup import SignUp
from services.responses.errors import CustomError
from services.responses.responses import CustomResponse

# Endpoint to handle the authentication functions
router = APIRouter(
    prefix='/api/v1',
)

# JWT expire time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 14*60

# Endpoint to create a new user - Patient or doctor
@router.post("/users")
async def login_for_access_token(
    user_type: str,
    user_data: SignUp    
    ):
    
    
    # Encrypt password
    user_data.password = Authentication().get_password_hash(user_data.password)
    
    # For patients
    if user_type == 'patient':
        sign_up = SignUpManager('patient')
        sign_up.create({
            'name': user_data.name,
            'email': user_data.email,
            'password': user_data.password,
            'cpf': user_data.cpf,
        })

    # For doctors
    elif user_type == 'doctor':
        sign_up = SignUpManager('doctor')
        sign_up.create(user_data.dict())

    else:
        raise CustomError().error_400('Wrong user type')

    # Return the Success response
    return CustomResponse().success_without_data()

