import requests
import random
import geocoder
from FlightRadar24 import FlightRadar24API
from airportsdata import load

# Global setup
fr_api = FlightRadar24API()
airports = load('IATA')
BLANK_FIELDS = ["", "N/A", "NONE"]

def get_current_gps_coordinates():
    g = geocoder.ip('me')
    return g.latlng if g.latlng else None

def get_flights_overhead():
    coordinates = get_current_gps_coordinates()
    print(coordinates)
    if not coordinates:
        print("❌ Cannot determine location.")
        return []

    lat, lon = coordinates
    bounds = fr_api.get_bounds_by_point(lat, lon, 11000)
    flights = fr_api.get_flights(bounds=bounds)
    data = []

    for flight in flights:
        details = fr_api.get_flight_details(flight)
        try:
            plane = details["aircraft"]["model"]["text"]
        except (KeyError, TypeError):
            plane = ""

        origin = (
            flight.origin_airport_iata
            if flight.origin_airport_iata and flight.origin_airport_iata.upper() not in BLANK_FIELDS
            else ""
        )

        destination = (
            flight.destination_airport_iata
            if flight.destination_airport_iata and flight.destination_airport_iata.upper() not in BLANK_FIELDS
            else ""
        )

        callsign = (
            flight.callsign
            if flight.callsign and flight.callsign.upper() not in BLANK_FIELDS
            else ""
        )

        data.append({
            "plane": plane,
            "origin": origin,
            "destination": destination,
            "vertical_speed": flight.vertical_speed,
            "altitude": flight.altitude,
            "callsign": callsign
        })

    return data

def print_flights(data):
    if not data:
        print("No flights overhead.")
        return

    for flight_data in data:
        print("✈️ Flight Info")
        print(f"Callsign:       {flight_data.get('callsign', 'N/A')}")
        print(f"Aircraft:       {flight_data.get('plane', 'Unknown')}")
        print(f"From:           {flight_data.get('origin', 'Unknown')}")
        print(f"To:             {flight_data.get('destination', 'Unknown')}")
        print(f"Altitude:       {flight_data.get('altitude', 'N/A')} ft")
        print(f"Vertical Speed: {flight_data.get('vertical_speed', 'N/A')} ft/min")
        print("-" * 40)

def airport_code_to_city(iata_code):
    airport = airports.get(iata_code.upper())
    return airport['city'] if airport else None

def guess_game(data):
    for i in data:
        guess_field = random.choice(['origin', 'destination'])
        known_field = 'origin' if guess_field == 'destination' else 'destination'

        guess_code = i[guess_field]
        known_code = i[known_field]

        known_city = airport_code_to_city(known_code)
        correct_city = airport_code_to_city(guess_code)

        if not correct_city or not known_city:
            print("✈️ Sorry, city info not found for one or both airports.")
            continue

        print("\n✈️  Guess the Flight Route!")
        print(f"Flight: {i['callsign']} ({i['plane']})")
        print(f"{known_field.capitalize()} city: {known_city}")
        print(f"{guess_field.capitalize()} city is missing.")

        guess = input(f"Guess the {guess_field} city: ").strip().lower()

        if guess == correct_city.lower():
            print("✅ Correct!\n")
        else:
            print(f"❌ Nope! The correct answer was {correct_city}.\n")

def main():
    print("🌍 Locating flights near you...")
    data = get_flights_overhead()

    if not data:
        print("No flights found. Try again later.")
        return

    #print_flights(data)
    guess_game(data)

if __name__ == "__main__":
    main()
