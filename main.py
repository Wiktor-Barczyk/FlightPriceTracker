import os
import requests
from datetime import datetime

# Jeśli używasz GitHub Actions z Secrets, pobierze go automatycznie.
# Jeśli testujesz na komputerze, wklej link bezpośrednio w cudzysłów poniżej.
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

ORIGIN = "KRK"          # Kod IATA lotniska wylotu (np. KRK, WAW, GDN)
DESTINATION = "CIA"     # Kod IATA lotniska powrotu (np. CIA, BGY, STN)
OUT_DATE = "2026-08-01" # Format: YYYY-MM-DD
IN_DATE = "2026-08-04"  # Format: YYYY-MM-DD
ADULTS = 2              # Liczba dorosłych
TARGET_PRICE = 1050     # Maksymalna cena łączna w PLN za WSZYSTKICH pasażerów

BOOKING_URL = (
    f"https://www.ryanair.com/pl/pl/trip/flights/select?"
    f"adults={ADULTS}&teens=0&children=0&infants=0&"
    f"dateOut={OUT_DATE}&dateIn={IN_DATE}&isConnectedFlight=false&"
    f"discount=0&promoCode=&isReturn=true&"
    f"originIata={ORIGIN}&destinationIata={DESTINATION}"
)

formatted_out_date = datetime.strptime(OUT_DATE, "%Y-%m-%d").strftime("%d.%m.%Y")
formatted_in_date = datetime.strptime(IN_DATE, "%Y-%m-%d").strftime("%d.%m.%Y")

def send_discord_alert(total_price, outbound_price, inbound_price):
    """Wysyła w pełni dynamiczną wiadomość na Discorda."""
    payload = {
        "username": "Łowca Promocji Ryanair",
        "avatar_url": "https://www.ryanair.com/favicon.ico",
        "embeds": [
            {
                "title": "🚨 CENA LOTU SPADŁA! ✈️",
                "description": (
                    f"Lot **{ORIGIN} ⇄ {DESTINATION}** dla **{ADULTS} os.** "
                    f"jest teraz dostępny w Twoim budżecie!"
                ),
                "color": 581478,
                "fields": [
                    {
                        "name": f"💰 Cena całkowita ({ADULTS} os.)",
                        "value": f"**{total_price:.2f} PLN** (Twój cel: {TARGET_PRICE} PLN)",
                        "inline": False
                    },
                    {
                        "name": f"📅 Wylot ({formatted_out_date})",
                        "value": f"{outbound_price:.2f} PLN / os.",
                        "inline": True
                    },
                    {
                        "name": f"📅 Powrót ({formatted_in_date})",
                        "value": f"{inbound_price:.2f} PLN / os.",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Kliknij nagłówek lub przycisk poniżej, aby przejść do rezerwacji"
                },
                "url": BOOKING_URL
            }
        ],
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "Kup lot na Ryanair.com",
                        "style": 5,
                        "url": BOOKING_URL
                    }
                ]
            }
        ]
    }
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code in [200, 204]:
        print("Powiadomienie pomyślnie wysłane na Discorda!")
    else:
        print(f"Błąd wysyłania na Discorda: {response.status_code}, {response.text}")

def check_ryanair_flights():
    """Odpytuje API Ryanair i sprawdza warunki cenowe."""
    api_url = (
        f"https://www.ryanair.com/api/booking/v4/pl-pl/availability?"
        f"ADT={ADULTS}&CHD=0&DateIn={IN_DATE}&DateOut={OUT_DATE}&"
        f"Destination={DESTINATION}&Origin={ORIGIN}&RoundTrip=true&ToUs=AGREED"
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(api_url, headers=headers)
        res.raise_for_status()
        data = res.json()
        
        outbound_trip = data['trips'][0]
        inbound_trip = data['trips'][1]
        
        # Wyciąganie najniższej ceny za 1 osobę
        min_outbound_pp = min(
            flight['regularFare']['fares'][0]['amount'] 
            for flight in outbound_trip['dates'][0]['flights'] 
            if 'regularFare' in flight
        )
        min_inbound_pp = min(
            flight['regularFare']['fares'][0]['amount'] 
            for flight in inbound_trip['dates'][0]['flights'] 
            if 'regularFare' in flight
        )
        
        # Obliczanie sumy za wszystkich pasażerów
        total_price = (min_outbound_pp + min_inbound_pp) * ADULTS
        
        print(f"Trasa: {ORIGIN} -> {DESTINATION} ({formatted_out_date} - {formatted_in_date})")
        print(f"Pasażerowie: {ADULTS} | Aktualna cena całkowita: {total_price:.2f} PLN")
        
        if total_price <= TARGET_PRICE:
            send_discord_alert(total_price, min_outbound_pp, min_inbound_pp)
        else:
            print(f"Cena przewyższa Twój cel ({TARGET_PRICE} PLN). Brak alertu.")
            
    except Exception as e:
        print(f"Błąd podczas pobierania danych z Ryanair: {e}")

if __name__ == "__main__":
    check_ryanair_flights()
