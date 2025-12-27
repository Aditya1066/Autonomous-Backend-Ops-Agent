from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_project(name: str, user_id: int, db: Session = Depends(get_db)):
    """
    Create a new project with the given name
    """
    project = Project(name=name, user_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project