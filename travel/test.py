from flask import Flask, render_template, request
import requests

# Flask app
app = Flask(__name__)

# Amadeus API credentials
CLIENT_ID = "m1UsydbjkM9DCi66OxAR24HEYgNZgiB3"
CLIENT_SECRET = "Im6ObXAp4piw4ZAz"
AUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_OFFERS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# Function to fetch access token
def get_access_token(client_id, client_secret):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(AUTH_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error obtaining access token: {response.status_code} - {response.json()}")
        return None

# Function to fetch flight offers
def fetch_flight_offers(access_token, origin, destination, departure_date, adults):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "nonStop": "false",  # Pass as a string
        "max": 5  # Limit the number of results
    }
    response = requests.get(FLIGHT_OFFERS_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching flight offers: {response.status_code} - {response.text}")
        return None

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    flight_offers = None
    error = None

    if request.method == "POST":
        # Get form data
        origin = request.form.get("origin").strip().upper()
        destination = request.form.get("destination").strip().upper()
        departure_date = request.form.get("departure_date").strip()
        adults = request.form.get("adults").strip()

        # Fetch access token
        access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        if access_token:
            # Fetch flight offers
            flight_offers = fetch_flight_offers(access_token, origin, destination, departure_date, adults)
        else:
            error = "Failed to retrieve access token."

    return render_template("index.html", flight_offers=flight_offers, error=error)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
