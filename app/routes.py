from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Endpoint, Check
from app.monitor import check_endpoint
from app.monitoring_service import run_and_store_check
from app.dependencies import status_rate_limit
from app.dependencies import check_now_rate_limit

from app.auth import get_current_user
from app.models import User
from app.cache import get_cached_status, set_cached_status, invalidate_status_cache




main_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@main_router.get("/check-now")
def check_now( _=Depends(check_now_rate_limit), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Trigger check for all endpoints in DB
    """

    endpoints = (
        db.query(Endpoint)
        .filter(Endpoint.user_id == current_user.id)
        .all()
    )

    results = []

    for endpoint in endpoints:
        result = run_and_store_check(endpoint, db)

        results.append(result)

    db.commit()

    invalidate_status_cache(current_user.id)

    return {"results": results}


@main_router.get("/status")
def get_status(_=Depends(status_rate_limit), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get latest status for each endpoint
    """

    cached = get_cached_status(current_user.id)
    if cached:
        return cached

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


    set_cached_status(current_user.id, response)

    return {"results": response}
