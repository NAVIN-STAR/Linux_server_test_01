from fastapi import FastAPI
from typing import List
from .database import Base, engine
from . import models
from .routes.coffee_routes import router as coffee_router
from .routes.auth_routes import router as auth_router
from dotenv import load_dotenv
import os

# Load .env from the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

Base.metadata.create_all(bind=engine)
APP_NAME = os.getenv("APP_NAME")
APP_ENV = os.getenv("APP_ENV")
app=FastAPI(root_path="/test01")
app.include_router(coffee_router)
app.include_router(auth_router)
@app.get("/")
async def root():
    return {
        "app_name": APP_NAME,
        "environment": APP_ENV,
        "message": "Welcome to the Coffee API! CI/CD. Checking the CI/CD pipeline with FastAPI and GitHub Actions."
    }


