from services.doctors.crud.agenda import AgendaManager
from services.sqs.main import SQSConnector
from services.doctors.crud.appointment import AppointmentManager



class ConsultationManager():
    
    def schedule(self):
        '''
        Schedule an consultation between doctor and patient
        '''
        sqs = SQSConnector()

        # Get the message from sqs
        message = sqs.receive_message()   
        
        if not message:
            print("No message")
            return None

        
        agenda_id = message['agenda_id']
        doctor_id = message['doctor_id']
        patient_id = message['patient_id']

        # Get the Agenda Object
        agenda = AgendaManager().get(agenda_id)


        if not agenda or agenda.doctor_id != doctor_id:
            return None

        
        # Create record in the appointment table
        apt = AppointmentManager()
        appointment = apt.create({
            'doctor_id': doctor_id,
            'patient_id': patient_id,
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

        # TODO Post a request to the payment queue
        sqs.send_message({
            'payment': 'ok'
        })

        return None


        
