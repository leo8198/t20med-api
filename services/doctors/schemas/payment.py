from typing import Optional
from pydantic import BaseModel

class PaymentDetails(BaseModel):
    number: Optional[str]
    cvv: Optional[str]
    expire_date: Optional[str]
    name: Optional[str]

class PaymentRequest(BaseModel):
    details: Optional[PaymentDetails]