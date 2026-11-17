from fastapi import FastAPI

app = FastAPI(
    title="FlightPriceTracker API",
    description="API for monitoring flight prices and tracking flight offers.",
    version="1.0.0",
)