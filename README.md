# FlightPriceTracker

FlightPriceTracker to projekt służący do monitorowania cen lotów i śledzenia dostępnych ofert. Projekt łączy skrypt automatycznie sprawdzający ceny lotów Ryanair z aplikacją webową opartą na FastAPI.

## Funkcjonalności

- Monitorowanie cen lotów Ryanair.
- Automatyczne sprawdzanie cen za pomocą GitHub Actions.
- Wysyłanie powiadomień Discord po wykryciu odpowiedniej oferty.
- REST API oparte na FastAPI.
- Endpoint zwracający informacje o stanie aplikacji.
- Endpoint zwracający listę przykładowych ofert lotów.
- Automatyczne testowanie aplikacji za pomocą pytest.

## Technologie

- Python 3.12
- FastAPI
- Uvicorn
- Requests
- Pytest
- HTTPX
- GitHub Actions
- Discord Webhooks

## Struktura projektu

```text
FlightPriceTracker/
├── .github/
│   └── workflows/
│       ├── check_flights.yml
│       └── ci.yml
├── app/
│   ├── routes/
│   │   ├── home.py
│   │   └── flights.py
│   ├── services/
│   └── main.py
├── tests/
│   └── test_api.py
├── main.py
├── requirements.txt
└── README.md
```

## Wymagania

Do uruchomienia projektu potrzebne są:

- Python 3.12
- Git

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone https://github.com/Wiktor-Barczyk/FlightPriceTracker.git
```

2. Przejdź do katalogu projektu:

```bash
cd FlightPriceTracker
```

3. Utwórz środowisko wirtualne:

```bash
python -m venv .venv
```

4. Aktywuj środowisko wirtualne.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Zainstaluj zależności:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Uruchamianie aplikacji FastAPI

Uruchom serwer poleceniem:

```bash
uvicorn app.main:app --reload
```

Aplikacja będzie dostępna pod adresem:

http://127.0.0.1:8000

## Endpointy API

| Metoda | Endpoint | Opis |
|---|---|---|
| GET | `/` | Informacje o stanie aplikacji |
| GET | `/flights` | Lista przykładowych ofert lotów |

### Dokumentacja API

FastAPI udostępnia automatyczną dokumentację Swagger:

http://127.0.0.1:8000/docs

Dokumentacja alternatywna:

http://127.0.0.1:8000/redoc

## Testy jednostkowe

Testy można uruchomić poleceniem:

```bash
python -m pytest -v
```

Testy sprawdzają poprawność odpowiedzi endpointów `/` oraz `/flights`.

## GitHub Actions

Projekt wykorzystuje dwa niezależne workflow:

### CI – ci.yml

- Automatyczne uruchamianie podczas Pull Requestów do gałęzi `main`.
- Instalacja zależności.
- Sprawdzanie składni kodu.
- Uruchamianie testów jednostkowych.
- Generowanie raportu testów.

### Monitorowanie cen – check_flights.yml

- Automatyczne uruchamianie skryptu monitorującego ceny Ryanair co godzinę.
- Możliwość ręcznego uruchomienia workflow.
- Wysyłanie powiadomień Discord.

Do działania powiadomień wymagany jest sekret `DISCORD_WEBHOOK_URL` skonfigurowany w ustawieniach repozytorium GitHub.

## Status projektu

Projekt jest rozwijany etapami. Aplikacja FastAPI udostępnia obecnie podstawowe endpointy API, a lista lotów zawiera przykładowe dane demonstracyjne.