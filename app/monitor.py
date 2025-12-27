import httpx
import time


def get_status_from_code(status_code: int | None) -> str:
    """
    Convert HTTP status code to health status.
    """
    if status_code is None:
        return "DOWN"
    if 200 <= status_code < 300:
        return "HEALTHY"
    if 400 <= status_code < 500:
        return "CLIENT_ERROR"
    return "SERVER_ERROR"


def check_endpoint(endpoint):
    """
    Takes an Endpoint SQLAlchemy object
    and checks its health.
    """
    start_time = time.time()

    try:
        response = httpx.get(endpoint.url, timeout=10)
        latency = time.time() - start_time

        return {
            "endpoint_id": endpoint.id,
            "status_code": response.status_code,
            "latency": round(latency, 2),
            "status": get_status_from_code(response.status_code),
        }

    except Exception:
        return {
            "endpoint_id": endpoint.id,
            "status_code": None,
            "latency": None,
            "status": "DOWN",
        }
