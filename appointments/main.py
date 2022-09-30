from fastapi import FastAPI
import sentry_sdk
from config import settings
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
from fastapi.middleware.cors import CORSMiddleware
from appointments.appointments import start



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

# Start scheduler
start()

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_checker():

    return {'detail':{
                'status':'ok',
                'status_code':0,
                'version': '1.0.0'},
            }