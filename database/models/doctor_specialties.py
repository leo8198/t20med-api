from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from sqlalchemy.ext.hybrid import hybrid_property


# Activities table
class DoctorSpecialty(Base):
    __tablename__ = "doctor_specialties"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    specialty_id = Column(Integer, ForeignKey("specialties.id"))
