from fastapi import FastAPI
from typing import List
from .database import Base, engine
from . import models
from .routes.coffee_routes import router as coffee_router
from .routes.auth_routes import router as auth_router
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)
APP_NAME = os.getenv("APP_NAME")
app=FastAPI(root_path="/test01")
app.include_router(coffee_router)
app.include_router(auth_router)
@app.get("/")
async def root():
    return {
        "app_name": APP_NAME
    }


