from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to FlightPriceTracker API!",
        "status": "running"
    }
