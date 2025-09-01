# 🧙 MTG Commander Deck Builder  

A **FastAPI web application** that helps Magic: The Gathering players manage their card collections, analyze them, and discover potential **Commander decks** they can build.  

The app integrates with:  
- **Scryfall API** – for card details (color identity, type, CMC, rarity, text).  
- **MTGGoldfish** – for real Commander archetypes & decklists.  

Upload your collection (CSV/XLSX) → get **commander suggestions, deck recommendations, and collection analytics**.  

---

## 🚀 Features

- **Collection Management**  
  - Upload CSV/XLSX file of your cards.  
  - Tracks **Quantity** and **Card Name** (two required columns).  

- **Commander Suggestions**  
  - Detects **Legendary Creatures** in your collection.  
  - Suggests them as potential commanders.  

- **Deck Recommendations**  
  - Compares your collection to **real meta decks** from MTGGoldfish.  
  - Shows **completion %** and lists missing cards.  

- **Collection Analytics**  
  - **Color Pie** (breakdown of color identity).  
  - **Type Distribution** (creature, instant, sorcery, etc.).  
  - **Mana Curve** (converted mana costs).  

---

## 📂 Project Structure

mtg_commander_app/
│── app.py # FastAPI app entry point
│── collection_manager.py # Collection parsing & summarizing
│── scryfall_api.py # Scryfall API integration
│── mtggoldfish_api.py # MTGGoldfish scraper
│── deck_suggestions.py # Deck matching logic
│── analytics.py # Generates charts (color pie, mana curve, etc.)
│── templates/ # Jinja2 templates (HTML pages)
│── static/ # CSS + generated charts
│ ├── style.css
│ ├── charts/
│── README.md # Project documentation


---

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/mtg-commander-app.git
cd mtg-commander-app
```

2. Install dependencies (Python 3.9+ recommended):

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn jinja2 pandas requests beautifulsoup4 matplotlib openpyxl
```

## ▶️ Running the App

Run the server:
```bash
uvicorn app:app --reload
```
If uvicorn isn’t recognized, run:
```bash
python -m uvicorn app:app --reload
```
Then open your browser at:
👉 http://127.0.0.1:8000

## 📥 Collection File Format
Your uploaded CSV/XLSX must have two columns in this order:

Quantity,Card Name
2,Sol Ring
1,Arcane Signet
4,Llanowar Elves

✔ Headers are case-insensitive (card name, Card name both work).
✔ Extra whitespace in headers is ignored.