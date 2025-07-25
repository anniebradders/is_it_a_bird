from flight_tracker import FlightTracker
from game import GuessTheCityGame

def main():
    print("🌍 Locating flights near you...")
    tracker = FlightTracker()
    data = tracker.get_flights_overhead()

    if not data:
        print("No flights found. Try again later.")
        return

    game = GuessTheCityGame()
    game.play(data)

if __name__ == "__main__":
    main()
