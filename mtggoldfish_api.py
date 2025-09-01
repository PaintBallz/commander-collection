import requests

BASE_URL = "https://www.mtggoldfish.com"

def fetch_commander_decklists():
    """
    Fetch commander deck archetypes using MTGGoldfish's JSON API.
    Returns list of dicts {name, url, cards}.
    """
    # MTGGoldfish commander metagame JSON
    url = f"{BASE_URL}/metagame/commander.json"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        print("Error fetching commander JSON:", resp.status_code)
        return []

    data = resp.json()
    decks = []

    # JSON contains archetypes with deck IDs
    for archetype in data.get("archetypes", [])[:10]:  # Limit to 10 decks
        deck_name = archetype.get("name", "Unknown Deck")
        deck_id = archetype.get("deck_id")

        if not deck_id:
            continue

        deck_url = f"{BASE_URL}/deck/{deck_id}"
        cards = fetch_decklist_json(deck_id)
        decks.append({"name": deck_name, "url": deck_url, "cards": cards})

    return decks

def fetch_decklist_json(deck_id: int):
    """
    Fetch decklist by deck_id using MTGGoldfish JSON.
    Returns list of card names.
    """
    url = f"{BASE_URL}/deck/download/json/{deck_id}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        print(f"Error fetching deck {deck_id} JSON:", resp.status_code)
        return []

    data = resp.json()
    cards = []

    # Cards are stored under "main"
    for entry in data.get("main", []):
        count = entry.get("count", 1)
        name = entry.get("name", "")
        for _ in range(count):
            cards.append(name)

    return cards
