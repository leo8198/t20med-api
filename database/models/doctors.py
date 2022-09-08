from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from sqlalchemy.ext.hybrid import hybrid_property


# Activities table
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    phone_number = Column(String)
    crm = Column(String)
    crm_state = Column(String)
    cpf = Column(String)
    rg_photo_front = Column(String)
    rg_photo_back = Column(String)
    crm_photo_front = Column(String)
    crm_photo_back = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    approved = Column(Boolean)
    banned = Column(Boolean)