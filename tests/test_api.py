from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to FlightPriceTracker API!",
        "status": "running"
    }


def test_flights_endpoint():
    response = client.get("/flights")

    assert response.status_code == 200

    data = response.json()

    assert "flights" in data
    assert len(data["flights"]) == 2

    first_flight = data["flights"][0]

    assert first_flight["departure"] == "Warsaw"
    assert first_flight["destination"] == "London"
    assert first_flight["airline"] == "Ryanair"
    assert first_flight["currency"] == "PLN"