from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)

    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
    endpoints = relationship("Endpoint", back_populates="project")

class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="endpoints")
    checks = relationship("Check", back_populates="endpoint")

class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True)
    status_code = Column(Integer, nullable=True)
    latency = Column(Float, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    endpoint_id = Column(Integer, ForeignKey("endpoints.id"))
    endpoint = relationship("Endpoint", back_populates="checks")
