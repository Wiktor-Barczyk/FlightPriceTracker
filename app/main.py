from fastapi import FastAPI
from app.routes import home

app = FastAPI(
    title="FlightPriceTracker API",
    description="API for monitoring flight prices and tracking flight offers.",
    version="1.0.0",
)

app.include_router(home.router)