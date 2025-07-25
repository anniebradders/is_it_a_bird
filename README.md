# ✈️ Is it a bird??

A little guessing game that shows real-time flights flying overhead using the FlightRadar24 API.  
Try to guess the **origin** or **destination** city of the planes above you!

---

## 🚀 How to Run

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the environment**:

    Windows:
   ```bash
   venv\Scripts\activate
   ```
    Mac:
   ```bash
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the game**:
   ```bash
   python main.py
   ```

## 🛠️ Future Plans

- [x] Split logic into **classes** and **modules** for better structure
- [x] Add a `requirements.txt` file for easier setup
- [ ] Build a simple **GUI** (e.g. with Tkinter or PyQt)
- [ ] Add a **retry/refresh option** if no flights are found



