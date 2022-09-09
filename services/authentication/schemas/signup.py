from typing import List, Optional
from pydantic import BaseModel

class SignUp(BaseModel):
    name: str 
    email: str 
    password: str 
    cpf: str 
    phone_number: Optional[str] 
    crm: Optional[str]
    crm_state: Optional[str] 


class DoctorDocuments(BaseModel):
    file_name: str 
    file_type: str 
    file_data: str

    
class SignUpDocuments(BaseModel):
    data: List[DoctorDocuments]