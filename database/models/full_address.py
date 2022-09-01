from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from sqlalchemy.ext.hybrid import hybrid_property


# Activities table
class FullAddress(Base):
    __tablename__ = "full_address"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    address = Column(String)
    address_number = Column(String)
    address_complement = Column(String)
    district = Column(String)
    city = Column(String)
    state = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())