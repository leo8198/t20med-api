import base64
from services.storage.local import LocalStorage
from services.storage.remote import RemoteStorage
from services.doctors.crud.doctors import DoctorManager
from services.authentication.crud.authentication import Authentication, User
from services.authentication.schemas.signup import SignUpDocuments 

class AuthenticationController():

    def sign_up_documents(
        self,
        current_user: User,
        user_data: SignUpDocuments
        ):
        '''
        Controller for the endpoint to send sign up documents
        '''        

        doctor = DoctorManager()
        doctor_obj = doctor.get(current_user.id)
        
        for data in user_data.data:
            
            
            # Update file name in the db
            doctor.update(
                doctor_obj,
                [
                    {
                        'key': data.file_type,
                        'value': data.file_name
                    }
                ]
            )

            # Upload file to S3
            RemoteStorage().save_file(
                data.file_name,
                base64.b64decode(data.file_data),
                f'doctors/{current_user.id}/',
                data.file_name,
                './uploads/',
                delete_after_upload=True
            )

        return None