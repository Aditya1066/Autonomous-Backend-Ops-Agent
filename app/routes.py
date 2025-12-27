from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Endpoint, Check
from app.monitor import check_endpoint
from app.monitoring_service import run_and_store_check


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/check-now")
def check_now(db: Session = Depends(get_db)):
    """
    Trigger check for all endpoints in DB
    """

    endpoints = db.query(Endpoint).all()
    results = []

    for endpoint in endpoints:
        result = run_and_store_check(endpoint, db)

        results.append(result)

    db.commit()

    return {"results": results}


@router.get("/status")
def get_status(db: Session = Depends(get_db)):
    """
    Get latest status for each endpoint
    """

    endpoints = db.query(Endpoint).all()
    response = []

    for endpoint in endpoints:
        latest = (
            db.query(Check)
            .filter(Check.endpoint_id == endpoint.id)
            .order_by(Check.created_at.desc())
            .first()
        )

        response.append({
            "endpoint": endpoint.name,
            "status": latest.status if latest else "UNKNOWN",
            "latency": latest.latency if latest else None
        })

    return {"results": response}
