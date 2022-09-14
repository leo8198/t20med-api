from services.doctors.crud.agenda import AgendaManager
from services.doctors.crud.doctors import DoctorManager
from services.doctors.crud.specialties import DoctorSpecialtiesManager, SpecialtiesManager
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from services.authentication.controllers.sign_up import AuthenticationController
from services.authentication.crud.authentication import Authentication, User
from services.responses.errors import CustomError
from services.responses.responses import CustomResponse
from database.models.agenda import Agenda
from services.doctors.schemas.agenda import AddAgenda

# Endpoint to handle the authentication functions
router = APIRouter(
    prefix='/api/v1',
)


# Create new doctors agenda
@router.post("/doctors/agenda")
async def post_agenda(
    agenda: AddAgenda,
    current_user: User = Depends(Authentication().get_doctor) 
):

    if current_user:
        
        for ag in agenda.days:

            AgendaManager().create(
                {
                    'time': ag.time,
                    'date': ag.date,
                    'doctor_id': current_user.id
                }
            )
        

        return CustomResponse().success_without_data()

    else:
        CustomError().error_403(
            'User not authorized to access this resource'
        )


# Delete doctor agenda
@router.delete("/doctors/agenda/{agenda_id}")
async def delete_agenda(
    agenda_id: int,
    current_user: User = Depends(Authentication().get_doctor) 
):

    if current_user:

        
        try:
            AgendaManager().delete(agenda_id,current_user.id)
        except Exception as e:
            print(e)
            return CustomError().error_500(
                "Error when deleting the agenda")

        return CustomResponse().success_without_data()

    else:
        CustomError().error_401("User not authenticated")