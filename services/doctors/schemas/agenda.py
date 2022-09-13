from typing import List
from pydantic import BaseModel

class Agenda(BaseModel):
    date: str # Format YYYY-mm-dd
    time: str # Format HH:MM

class AddAgenda(BaseModel):
    days: List[Agenda] 