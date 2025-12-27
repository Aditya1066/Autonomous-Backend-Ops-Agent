import uvicorn
from fastapi import FastAPI
from app.routes import router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Endpoint Monitor API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    router,
    prefix="/api",
    tags=["monitoring"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)