from utils import BLANK_FIELDS

class Flight:
    def __init__(self, callsign, plane, origin, destination, altitude, vertical_speed):
        self.callsign = callsign
        self.plane = plane
        self.origin = origin
        self.destination = destination
        self.altitude = altitude
        self.vertical_speed = vertical_speed

    @staticmethod
    def from_api(api_flight, plane):
        def clean(value):
            return value if value and value.upper() not in BLANK_FIELDS else ""

        return Flight(
            callsign=clean(api_flight.callsign),
            plane=plane,
            origin=clean(api_flight.origin_airport_iata),
            destination=clean(api_flight.destination_airport_iata),
            altitude=api_flight.altitude,
            vertical_speed=api_flight.vertical_speed,
        )
