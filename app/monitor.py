import httpx
import time

def check_endpoint(endpoint):
    """
    Check a single API endpoint
    Returns result as Dict
    """
    url = endpoint["url"]
    name = endpoint["name"]

    start_time = time.time()

    try:
        response = httpx.get(url, timeout=5)
        latency = time.time() - start_time

        return {
            "name" : name,
            "url": url,
            "status_code": response.status_code,
            "latency": latency,
            "status": get_status(response.status_code)
        }
    
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "status_code": None,
            "latency": None,
            "status": "DOWN",
        }
    
def get_status(status_code):
    """
    Determine status based on HTTP status code
    """
    if status_code is None:
        return "DOWN"
    elif 200 <= status_code < 300:
        return "UP"
    elif 400 <= status_code < 500:
        return "CLIENT ERROR"
    elif 500 <= status_code < 600:
        return "SERVER ERROR"
    else:
        return "UNKNOWN"