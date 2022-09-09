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

# Get doctors agenda from a given specialty
@router.get("/doctors/specialties/{specialty_id}")
async def get_specialty_doctors(
    specialty_id: int
):
    # Get doctors from a given specialty
    doctors = DoctorSpecialtiesManager().get_by_specialty(specialty_id)

    
    if not doctors:
        return CustomError().error_404(
            'No doctors availables for this specialty'
        )

    agenda = []
    for doctor in doctors:
        
        # Get doctor Agenda
        doctor_agenda = AgendaManager().get_agenda(doctor.doctor_id)

        # Get doctor personal data
        doctor_data = DoctorManager().get(doctor.doctor_id)

        agenda.append(
            {   
                "personal_data": {
                    "id": doctor_data.id,
                    "name": doctor_data.name,
                    "crm": doctor_data.crm,
                    "crm_state": doctor_data.crm_state
                },
                "agenda": AgendaManager().group_by_date(doctor_agenda)
            }
        )
        
    
    return CustomResponse().success_with_data(agenda)
