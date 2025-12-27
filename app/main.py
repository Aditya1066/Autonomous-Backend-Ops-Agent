import uvicorn
from fastapi import FastAPI
from app.routes import router
from app.database import engine
from app import models

from app.background_monitor import monitoring_loop
from contextlib import asynccontextmanager
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    models.Base.metadata.create_all(bind=engine)

    monitor_thread = threading.Thread(
        target=monitoring_loop,
        daemon=True
    )
    monitor_thread.start()

    yield  

    # --- SHUTDOWN ---


app = FastAPI(title="Backend Monitoring Service", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    router,
    prefix="/api"
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)