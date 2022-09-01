from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from sqlalchemy.ext.hybrid import hybrid_property


# Activities table
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    cpf = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())