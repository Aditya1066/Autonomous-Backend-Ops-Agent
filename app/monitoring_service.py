from sqlalchemy.orm import Session
from app.models import Check
from app.monitor import check_endpoint


def run_and_store_check(endpoint, db: Session):
    """
    Run checks for all endpoints and store results in the database
    """

    result = check_endpoint(endpoint)


    check = Check(
        endpoint_id=endpoint.id,
        status_code=result["status_code"],
        latency=result["latency"],
        status=result["status"],
    )

    db.add(check)

    return result