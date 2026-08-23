from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import os

from app.database.database import engine, Base

from app.models import User

from app.routes import auth


app = FastAPI()


# Create database tables.
Base.metadata.create_all(bind=engine)


# Required by Authlib for OAuth state/session handling.
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)


app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }