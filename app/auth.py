from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> User:
    user = (
        db.query(User)
        .filter(User.api_key == x_api_key)
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user
