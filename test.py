import requests
import time

# Amadeus API credentials
API_KEY = "GwyuqTTGWbwt9nqV6IOr3GkDazPQrjAi"
API_SECRET = "akLIj4yQGt765zxg"

def parse_and_display_flights(flight_data):
    if not flight_data or "data" not in flight_data:
        print("No flight offers available.")
        return

    print(f"Total Offers Found: {len(flight_data['data'])}")
    for offer in flight_data['data']:
        print("\n" + "=" * 40)
        print(f"Flight Offer ID: {offer['id']}")
        
        # Price information
        price = offer["price"]
        print(f"Price: {price['grandTotal']} {price['currency']}")
        
        # Itinerary details
        for itinerary_index, itinerary in enumerate(offer["itineraries"], start=1):
            print(f"\nItinerary {itinerary_index}: Duration - {itinerary['duration']}")
            for segment_index, segment in enumerate(itinerary["segments"], start=1):
                print(f"  Segment {segment_index}:")
                print(f"    Flight: {segment['carrierCode']}{segment['number']}")
                print(f"    Departure: {segment['departure']['iataCode']} at {segment['departure']['at']}")
                print(f"    Arrival: {segment['arrival']['iataCode']} at {segment['arrival']['at']}")
                print(f"    Duration: {segment['duration']}")
                print(f"    Aircraft: {segment['aircraft']['code']}")

        # Traveler pricing (optional, for more detail)
        if "travelerPricings" in offer:
            print("\nTraveler Pricing:")
            for traveler in offer["travelerPricings"]:
                print(f"  Type: {traveler['travelerType']} | Fare: {traveler['fareOption']}")
                traveler_price = traveler["price"]
                print(f"    Total Price: {traveler_price['total']} {traveler_price['currency']}")
        
        print("=" * 40)


# Example use
if __name__ == "__main__":
    # Assume `flight_data` is the JSON response from the API
    flight_data = {
        "meta": {"count": 30},
        "data": [
            {
                "id": "1",
                "price": {"grandTotal": "145.76", "currency": "EUR"},
                "itineraries": [
                    {
                        "duration": "PT8H25M",
                        "segments": [
                            {
                                "carrierCode": "F9",
                                "number": "4206",
                                "departure": {"iataCode": "ONT", "at": "2025-02-01T20:35:00"},
                                "arrival": {"iataCode": "LAS", "at": "2025-02-01T21:59:00"},
                                "duration": "PT1H24M",
                                "aircraft": {"code": "321"},
                            },
                            {
                                "carrierCode": "F9",
                                "number": "3238",
                                "departure": {"iataCode": "LAS", "at": "2025-02-01T23:54:00"},
                                "arrival": {"iataCode": "JFK", "at": "2025-02-02T08:00:00"},
                                "duration": "PT5H6M",
                                "aircraft": {"code": "32Q"},
                            },
                        ],
                    }
                ],
                "travelerPricings": [
                    {
                        "travelerType": "ADULT",
                        "fareOption": "STANDARD",
                        "price": {"total": "145.76", "currency": "EUR"},
                    }
                ],
            }
        ],
    }
    parse_and_display_flights(flight_data)
