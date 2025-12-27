from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Endpoint

router = APIRouter(prefix="/endpoints", tags=["endpoints"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_endpoint(name: str,url: str, project_id: int, db: Session = Depends(get_db)):
    """
    Add a new endpoint to be monitored
    """
    endpoint = Endpoint(name=name, url=url, project_id=project_id)
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)
    return endpoint