from fastapi import FastAPI

from app.database.database import engine, Base
from app.models import User
from app.routes import auth

app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }