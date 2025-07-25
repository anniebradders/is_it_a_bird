import tkinter as tk
from tkinter import messagebox
import json
import os
from flight_tracker import FlightTracker
from utils import airport_code_to_city

SCORES_FILE = "scores.json"


class FlightGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the City")
        self.root.geometry("460x400")
        self.root.configure(bg="#1e1e1e")

        self.username = None
        self.points = 0
        self.flight_index = 0
        self.current_flight = None

        self.tracker = FlightTracker()
        self.flights = self.tracker.get_flights_overhead()

        self.load_scores()
        self.create_welcome_screen()

    def load_scores(self):
        if not os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "w") as f:
                json.dump({}, f)

        with open(SCORES_FILE, "r") as f:
            self.scores = json.load(f)

    def create_welcome_screen(self):
        self.clear_window()

        self.title_label = tk.Label(self.root, text="Welcome to Guess the City", font=("Helvetica", 16),
                                    bg="#1e1e1e", fg="white")
        self.title_label.pack(pady=30)

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 14), bg="#2b2b2b", fg="white",
                                   insertbackground="white", relief="flat", justify="center")
        self.name_entry.pack(ipady=6, ipadx=6, pady=10)
        self.name_entry.focus()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game,
                                      font=("Helvetica", 10), bg="#3a3a3a", fg="white", relief="flat",
                                      activebackground="#505050", padx=10, pady=5)
        self.start_button.pack(pady=10)

    def start_game(self):
        name = self.name_entry.get().strip().title()
        if not name:
            messagebox.showwarning("Name Required", "Please enter your name.")
            return

        self.username = name
        if name not in self.scores:
            self.scores[name] = 0
        self.points = self.scores[name]

        self.create_game_screen()
        self.next_flight()

    def create_game_screen(self):
        self.clear_window()

        self.title_label = tk.Label(self.root, text="Guess the City", font=("Helvetica", 16),
                                    bg="#1e1e1e", fg="white")
        self.title_label.pack(pady=15)

        self.flight_info = tk.Label(self.root, text="", bg="#1e1e1e", fg="#e0e0e0",
                                    font=("Helvetica", 12), justify="center")
        self.flight_info.pack(pady=10)

        self.input_entry = tk.Entry(self.root, font=("Helvetica", 12), bg="#2b2b2b", fg="white",
                                    insertbackground="white", relief="flat", justify="center")
        self.input_entry.pack(ipady=6, ipadx=6, pady=10)
        self.input_entry.bind("<Return>", lambda event: self.check_guess())

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#1e1e1e")
        self.result_label.pack(pady=5)

        self.buttons_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.buttons_frame.pack(pady=10)

        self.submit_button = tk.Button(self.buttons_frame, text="Submit Guess", command=self.check_guess,
                                       font=("Helvetica", 10), bg="#3a3a3a", fg="white", relief="flat",
                                       activebackground="#505050", padx=10, pady=5)
        self.submit_button.pack(side="left", padx=10)

        self.next_button = tk.Button(self.buttons_frame, text="Next Flight", command=self.next_flight,
                                     font=("Helvetica", 10), bg="#3a3a3a", fg="white", relief="flat",
                                     activebackground="#505050", padx=10, pady=5, state="disabled")
        self.next_button.pack(side="left", padx=10)

        self.footer = tk.Frame(self.root, bg="#1e1e1e")
        self.footer.pack(side="bottom", fill="x", pady=15)

        self.score_label = tk.Label(self.footer, text=f"{self.username} | Score: {self.points}",
                                    font=("Helvetica", 10), bg="#1e1e1e", fg="#888888")
        self.score_label.pack()

        self.quit_button = tk.Button(self.footer, text="Exit", command=self.exit_game,
                                     font=("Helvetica", 10), bg="#2b2b2b", fg="white", relief="flat",
                                     activebackground="#444444", padx=10, pady=3)
        self.quit_button.pack(pady=6)

    def display_flight(self, flight, guess_field, known_field):
        known_city = airport_code_to_city(getattr(flight, known_field))
        if not known_city:
            self.next_flight()
            return

        self.current_flight = {
            "flight": flight,
            "guess_field": guess_field,
            "known_field": known_field,
            "correct_city": airport_code_to_city(getattr(flight, guess_field))
        }

        if not self.current_flight["correct_city"]:
            self.next_flight()
            return

        self.flight_info.config(
            text=f"Flight: {flight.callsign} ({flight.plane})\n{known_field.capitalize()} city: {known_city}\nGuess the {guess_field} city:"
        )
        self.input_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.next_button.config(state="disabled")
        self.submit_button.config(state="normal")

    def next_flight(self):
        if self.flight_index >= len(self.flights):
            messagebox.showinfo("End", "No more flights found.")
            self.exit_game()
            return

        import random
        flight = self.flights[self.flight_index]
        self.flight_index += 1

        guess_field = random.choice(["origin", "destination"])
        known_field = "origin" if guess_field == "destination" else "destination"

        self.display_flight(flight, guess_field, known_field)

    def check_guess(self):
        guess = self.input_entry.get().strip().lower()
        correct = self.current_flight["correct_city"]

        if not guess:
            return

        if guess == correct.lower():
            self.result_label.config(text="Correct!", fg="#6ee7b7")
            self.points += 1
        else:
            self.result_label.config(text=f"Incorrect — it was {correct}", fg="#f87171")

        self.score_label.config(text=f"{self.username} | Score: {self.points}")
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")

    def exit_game(self):
        self.scores[self.username] = self.points
        with open(SCORES_FILE, "w") as f:
            json.dump(self.scores, f, indent=2)
        self.root.destroy()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightGameGUI(root)
    root.mainloop()
