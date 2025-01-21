import requests
import json

# Amadeus API credentials
CLIENT_ID = "m1UsydbjkM9DCi66OxAR24HEYgNZgiB3"  # Replace with your Amadeus client ID
CLIENT_SECRET = "Im6ObXAp4piw4ZAz"  # Replace with your Amadeus client secret
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
        "nonStop": "false",  
        "max": 5  
    }
    
    response = requests.get(FLIGHT_OFFERS_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching flight offers: {response.status_code} - {response.text}")
        return None

# Function to parse and display flight offers
def display_flight_offers(data):
    if not data or "data" not in data:
        print("No flight offers found.")
        return
    
    for index, offer in enumerate(data["data"], start=1):
        print(f"\nFlight Offer {index}:")
        itinerary = offer["itineraries"][0]
        price = offer["price"]["total"]
        
        print(f"  Price: {price} {offer['price']['currency']}")
        print(f"  Duration: {itinerary['duration']}")
        
        for segment in itinerary["segments"]:
            departure = segment["departure"]
            arrival = segment["arrival"]
            print(f"    Flight: {segment['carrierCode']}{segment['number']}")
            print(f"      From: {departure['iataCode']} at {departure['at']}")
            print(f"      To: {arrival['iataCode']} at {arrival['at']}")
            print(f"      Aircraft: {segment['aircraft']['code']}")
        print("-" * 50)

# Main function
if __name__ == "__main__":
    # Get user input for flight search
    print("Welcome to the Flight Search Tool!")
    origin = input("Enter origin airport code (e.g., LAX): ").strip().upper()
    destination = input("Enter destination airport code (e.g., JFK): ").strip().upper()
    departure_date = input("Enter departure date (YYYY-MM-DD): ").strip()
    adults = int(input("Enter the number of adults (1 or more): ").strip())

    print("\nFetching access token...")
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    
    if access_token:
        print("Access token obtained successfully!")
        print("\nFetching flight offers...\n")
        flight_data = fetch_flight_offers(access_token, origin, destination, departure_date, adults)
        display_flight_offers(flight_data)
    else:
        print("Failed to retrieve access token. Exiting...")
