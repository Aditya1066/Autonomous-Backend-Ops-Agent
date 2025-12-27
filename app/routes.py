from fastapi import APIRouter
from app.config import ENDPOINTS
from app.monitor import check_endpoint

router = APIRouter()

latest_results = []

@router.get("/status")
async def get_status():
    """
    Get the latest status of all monitored endpoints
    """
    return {"results": latest_results}

@router.get("/check-now")
async def check_now():
    """
    Trigger an immediate check of all monitored endpoints
    """
    global latest_results

    results = []
    for endpoint in ENDPOINTS:
        result = check_endpoint(endpoint)
        results.append(result)

    latest_results = results
    return {"message": "Endpoints checked", "results": latest_results}