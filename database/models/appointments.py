from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from sqlalchemy.ext.hybrid import hybrid_property


# Activities table
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String)
    date = Column(String)
    time = Column(String)
    status = Column(Integer)
    rate = Column(Integer)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
