"""Main module for the FastAPI application."""

import sentry_sdk
from fastapi import FastAPI

from src.api.health_check import router as health_check_router

# Import the router from the api module
from src.api.root import router as root_router
from src.api.v1.routers import router as api_v1_router

sentry_sdk.init(
    dsn="https://35eaf99e376366bbc188823c020c76ec@o208781.ingest.us.sentry.io/4507466637312000",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# Set up the FastAPI app
app = FastAPI()

# Include the router in the app
app.include_router(root_router)
# Include the api_v1_router in the app
app.include_router(api_v1_router, prefix="/api/v1")
# Include the health_check_router in the app
app.include_router(health_check_router)
