from fastapi import FastAPI
from app.routes import router
import uvicorn

app = FastAPI(title="Endpoint Monitor API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    router,
    prefix="/api/v1",
    tags=["monitoring"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)