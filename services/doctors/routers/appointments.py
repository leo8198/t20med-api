from services.doctors.crud.specialties import SpecialtiesManager
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


# Get all doctor specialties
@router.get("/doctors/specialties")
async def get_specialties():

    return CustomResponse().success_with_data(
        SpecialtiesManager().get_all()
     )
