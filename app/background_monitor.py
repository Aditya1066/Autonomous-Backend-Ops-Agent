import time
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Endpoint
from app.monitoring_service import run_and_store_check
from app.config import CHECK_INTERVAL_SECONDS

def monitoring_loop():
    """
    Background monitoring loop that checks all endpoints at regular intervals
    """
    while True:
        db: Session = SessionLocal()
        try:
            endpoints = db.query(Endpoint).all()

            for endpoint in endpoints:
                run_and_store_check(endpoint, db)

            db.commit()
        except Exception as e:
            print(f"Error during monitoring loop: {e}")
        finally:
            db.close()

        time.sleep(CHECK_INTERVAL_SECONDS)