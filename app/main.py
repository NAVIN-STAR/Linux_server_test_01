from fastapi import FastAPI
from typing import List
from .database import Base, engine
from . import models
from .routes.coffee_routes import router as coffee_router
from .routes.auth_routes import router as auth_router


Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(coffee_router)
app.include_router(auth_router)



