from services.doctors.crud.agenda import AgendaManager
from services.doctors.crud.doctors import DoctorManager
from services.doctors.crud.appointment import AppointmentManager
from services.doctors.crud.payments import PaymentManager
from services.doctors.crud.specialties import DoctorSpecialtiesManager, SpecialtiesManager
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from services.authentication.controllers.sign_up import AuthenticationController
from services.authentication.crud.authentication import Authentication, User
from services.payments.connectors.payments import PaymentConector
from services.responses.errors import CustomError
from services.responses.responses import CustomResponse
from services.doctors.schemas.payment import PaymentRequest
from services.sqs.main import SQSConnector

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

# Schedule an consultation
@router.post("/doctors/{doctor_id}/{agenda_id}")
async def post_doctors_consultation(
    doctor_id: int,
    agenda_id: int,
    payment: str,
    specialty_id: int,
    payment_info: PaymentRequest,
    current_user: User = Depends(Authentication().get_patient) 
):

    if current_user:

        # Get the Agenda Object
        agenda = AgendaManager().get(agenda_id)


        if not agenda or agenda.doctor_id != doctor_id:
            return CustomError().error_404(
                "Agenda timetable doesn't exist"
            )

        sqs = SQSConnector('appointments.fifo')
        sqs.send_message({
            'agenda_id': agenda_id,
            'doctor_id': doctor_id,
            'patient_id': current_user.id,
            'specialty_id': specialty_id
        })

        return CustomResponse().success_without_data()

        
        # Create record in the appointment table
        apt = AppointmentManager()
        appointment = apt.create({
            'doctor_id': doctor_id,
            'patient_id': current_user.id,
            'date': agenda.date,
            'time': agenda.time,
            'status': apt.get_status('pending_payment'),
            'call_id': apt.generate_id()
        })


        # Delete from agenda table
        AgendaManager().delete(
            agenda.id,
            doctor_id
        )

        # Get specialty price
        specialty = SpecialtiesManager().get(specialty_id)

        # Create the payment order
        pay = PaymentManager()
        pay.create({
            'appointment_id': appointment.id,
            'type': pay.payment_type_number(payment),
            'status': pay.payment_status('pending'),
            'value': specialty.price,
            'received_at': datetime.now()
        })
        

        # Do the payment
        payment_status = PaymentConector().create_transaction(
            payment,
            specialty.price,
            payment_info.details
        )

        return CustomResponse().success_with_data(
            {
                "payment": payment_status
            }
        )



    else:
        return CustomError().error_401(
            'User not authenticated'
        )