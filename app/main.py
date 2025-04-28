import json

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)
app.include_router(main_router)


def custom_openapi():
    with open('openapi.json', 'r') as file:
        return json.load(file)


# app.openapi = custom_openapi
