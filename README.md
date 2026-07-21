# FlightPriceChecker

A simple Python script integrated with GitHub Actions and Discord that automatically tracks selected Ryanair flight prices and sends a Discord notification when the price drops below a set threshold.

## Features

- automatic tracking of round-trip flight prices directly from the official Ryanair API,
- Discord channel notifications (Discord Webhook) with a breakdown of price per person and total cost,
- a direct button in the Discord message redirecting straight to ticket booking,
- full cloud automation using GitHub Actions (runs every hour without keeping your PC on),
- flexible configuration of flight parameters (route, dates, number of passengers, budget) in one place.

## Keys and Webhook Configuration

The application loads the Webhook URL from the `DISCORD_WEBHOOK_URL` environment variable stored in secure GitHub Secrets.

### Step 1: Generating a Discord Webhook
1. Open your Discord server.
2. Go to **Edit Channel** (the gear icon next to the channel name) ➔ **Integrations** ➔ **Webhooks**.
3. Click **New Webhook**, name it e.g., `FlightPriceChecker`, and click **Copy Webhook URL**.

### Step 2: Configuring GitHub Secrets
1. Go to your GitHub repository.
2. Navigate to: **Settings** ➔ **Secrets and variables** (under the *Security* section) ➔ **Actions**.
3. Click **New repository secret**.
4. Set the parameters:
   - **Name:** `DISCORD_WEBHOOK_URL`
   - **Secret:** *(paste the copied URL from Discord)*
5. Save by clicking **Add secret**.

### Step 3: Configuring flight parameters in the code
You can set all flight parameters directly at the top of the `main.py` file:

```python
ORIGIN = "KRK"          # IATA code of the departure airport (e.g., KRK)
DESTINATION = "CIA"     # IATA code of the destination airport (e.g., CIA)
OUT_DATE = "2026-08-01" # Departure date (Format: YYYY-MM-DD)
IN_DATE = "2026-08-04"  # Return date (Format: YYYY-MM-DD)
ADULTS = 2              # Number of adult passengers
TARGET_PRICE = 1050     # Maximum total price in PLN for all passengers
```

## Execution (GitHub Actions)

The script runs automatically every hour on GitHub servers.

If you want to force an immediate price check on demand:
1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Ryanair Price Check** workflow from the left list.
3. Click the **Run workflow** button on the right side.

## Project Structure

```text
FlightPriceChecker/
├─ main.py
├─ README.md
└─ .github/
   └─ workflows/
      └─ check_flights.yml
```

## How it works

1. GitHub Actions runs the `main.py` script automatically in the background every hour (using a Cron schedule).
2. The script retrieves the `DISCORD_WEBHOOK_URL` address from secure GitHub secrets.
3. The backend sends an HTTP GET request directly to the internal Ryanair API using the selected route and date parameters.
4. The script extracts the lowest fares for the outbound and inbound flights and calculates the total cost for the specified number of passengers.
5. If the total price is lower than or equal to the `TARGET_PRICE`, the script generates an Embed card and sends a notification to your Discord channel with a booking button.
