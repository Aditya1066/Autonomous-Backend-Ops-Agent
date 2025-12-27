import secrets
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

users_router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@users_router.post("/")
def create_user(email: str, db: Session = Depends(get_db)):
    api_key = secrets.token_hex(16)

    user = User(
        email=email,
        api_key=api_key
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "api_key": api_key  
    }