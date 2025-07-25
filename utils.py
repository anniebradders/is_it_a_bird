from airportsdata import load

BLANK_FIELDS = ["", "N/A", "NONE"]
_airports = load('IATA')

def airport_code_to_city(iata_code):
    airport = _airports.get(iata_code.upper())
    return airport['city'] if airport else None
