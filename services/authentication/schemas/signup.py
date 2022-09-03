from typing import Optional
from pydantic import BaseModel

class SignUp(BaseModel):
    name: str 
    email: str 
    password: str 
    cpf: str 
    phone_number: Optional[str] 
    crm: Optional[str]
    crm_state: Optional[str] 