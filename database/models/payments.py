from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from sqlalchemy.ext.hybrid import hybrid_property


# Activities table
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer)
    type = Column(Integer)
    value = Column(Float)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    received_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
