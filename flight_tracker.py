import geocoder
from FlightRadar24 import FlightRadar24API
from models import Flight
from utils import BLANK_FIELDS

class FlightTracker:
    def __init__(self):
        self.fr_api = FlightRadar24API()

    def _get_current_coordinates(self):
        g = geocoder.ip('me')
        return g.latlng if g.latlng else None

    def get_flights_overhead(self):
        coords = self._get_current_coordinates()
        if not coords:
            print("❌ Cannot determine location.")
            return []

        lat, lon = coords
        bounds = self.fr_api.get_bounds_by_point(lat, lon, 7000)
        flights = self.fr_api.get_flights(bounds=bounds)

        result = []
        for flight in flights:
            details = self.fr_api.get_flight_details(flight)
            try:
                plane = details["aircraft"]["model"]["text"]
            except (KeyError, TypeError):
                plane = ""

            result.append(Flight.from_api(flight, plane))
        return result
