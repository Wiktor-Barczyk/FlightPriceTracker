
from fastapi import APIRouter

router = APIRouter()


@router.get("/flights")
def get_flights():
    return {
        "flights": [
            {
                "id": 1,
                "departure": "Warsaw",
                "destination": "London",
                "airline": "Ryanair",
                "price": 199.99,
                "currency": "PLN"
            },
            {
                "id": 2,
                "departure": "Krakow",
                "destination": "Rome",
                "airline": "Ryanair",
                "price": 249.99,
                "currency": "PLN"
            }
        ]
    }