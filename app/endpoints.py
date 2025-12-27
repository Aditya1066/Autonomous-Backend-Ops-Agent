from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Endpoint
from app.auth import get_current_user
from app.models import User

endpoints_router = APIRouter(prefix="/endpoints", tags=["endpoints"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@endpoints_router.post("/")
def add_endpoint(name: str,
    url: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    """
    Add a new endpoint to be monitored
    """

    endpoint = Endpoint(
        name=name,
        url=url,
        user_id=current_user.id
    )

    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)

    return endpoint