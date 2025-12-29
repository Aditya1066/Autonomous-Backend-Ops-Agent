from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    api_key = Column(String, unique=True, index=True)



class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User")

    checks = relationship("Check", back_populates="endpoint",cascade="all, delete-orphan")

class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True)
    status_code = Column(Integer, nullable=True)
    latency = Column(Float, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    endpoint_id = Column(Integer, ForeignKey("endpoints.id"))
    endpoint = relationship("Endpoint", back_populates="checks")
