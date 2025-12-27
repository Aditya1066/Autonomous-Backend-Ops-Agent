# Backend Monitor

A simple FastAPI app that checks backend APIs and reports health status.

## Run
pip install -r requirements.txt
uvicorn app.main:app --reload

## Endpoints
- GET /check-now
- GET /status
