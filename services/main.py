from fastapi import FastAPI, status, Request
import os 
import sys 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from services.authentication.routers.login import router as login_router
from services.authentication.routers.reset_password import router as reset_password_router
from services.authentication.routers.sign_up import router as sign_up_router
from services.health import router as health_router
from services.doctors.routers.appointments import router as appointments_router
from services.doctors.routers.agenda import router as agenda_router
import sentry_sdk
from config import settings
from sentry_sdk.integrations.logging import LoggingIntegration
import logging


# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=settings.sentry_api_url,
    traces_sample_rate=1.0,
    integrations=[
        sentry_logging,
    ],
)

app = FastAPI(
    title = 'T20Med-API',
    version='1.0.8',
)

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Handle data model error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": {
            "status": "Error",
            "status_code": 4,
            "description": "Formato do JSON enviado está incorreto"
        },
                 }),
    )

# Routers
app.include_router(login_router)
app.include_router(reset_password_router)
app.include_router(sign_up_router)
app.include_router(health_router)
app.include_router(appointments_router)
app.include_router(agenda_router)