from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(email: str, db: Session = Depends(get_db)):
    """
    Create a new user with the given email
    """
    user = User(email=email)
    db.add(user) 
    db.commit()
    db.refresh(user)
    return user