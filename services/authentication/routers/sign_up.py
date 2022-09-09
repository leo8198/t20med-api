import base64
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from services.authentication.controllers.sign_up import AuthenticationController
from services.authentication.crud.authentication import Authentication, User
from services.authentication.crud.signup import SignUpManager
from services.authentication.schemas.signup import SignUp, SignUpDocuments
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
async def sign_up(
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
            'banned': False
        })

    # For doctors
    elif user_type == 'doctor':
        sign_up = SignUpManager('doctor')
        data = user_data.dict()
        data['approved'] = False
        data['banned'] = False
        sign_up.create(data)

    else:
        raise CustomError().error_400('Wrong user type')

    # Return the Success response
    return CustomResponse().success_without_data()


# Send documents for doctor sign up
@router.post("/users/documents")
async def send_authentication_documents(
    user_data: SignUpDocuments,
    background_task: BackgroundTasks,
    current_user: User = Depends(Authentication().get_doctor) 
    ):

    if current_user:

        # If the user is a doctor        
        if Authentication().is_doctor(current_user):
           
            # Do the task in the background
            background_task.add_task(
                AuthenticationController().sign_up_documents,
                current_user,
                user_data
            )
            
        # If it's not a doctor
        else:
            return CustomError().error_403(
                'User not authorized to access this resource'
            )

        return CustomResponse().success_without_data()



        

    else:

        return CustomError().error_401(
            'User not authenticated'
        )

