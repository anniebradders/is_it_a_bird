import random
from utils import airport_code_to_city

class GuessTheCityGame:
    def play(self, flights):
        for flight in flights:
            guess_field = random.choice(['origin', 'destination'])
            known_field = 'origin' if guess_field == 'destination' else 'destination'

            guess_code = getattr(flight, guess_field)
            known_code = getattr(flight, known_field)

            known_city = airport_code_to_city(known_code)
            correct_city = airport_code_to_city(guess_code)

            if not correct_city or not known_city:
                print("✈️ Sorry, city info not found for one or both airports.")
                continue

            print("\n✈️  Guess the Flight Route!")
            print(f"Flight: {flight.callsign} ({flight.plane})")
            print(f"{known_field.capitalize()} city: {known_city}")
            print(f"{guess_field.capitalize()} city is missing.")

            guess = input(f"Guess the {guess_field} city: ").strip().lower()

            if guess == correct_city.lower():
                print("✅ Correct!\n")
            else:
                print(f"❌ Nope! The correct answer was {correct_city}.\n")
