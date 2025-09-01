import requests

def fetch_card_data(name: str):
    """Fetch card info from Scryfall API."""
    url = f"https://api.scryfall.com/cards/named?fuzzy={name}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return {
            "name": data["name"],
            "colors": data.get("color_identity", []),
            "type": data.get("type_line", ""),
            "oracle_text": data.get("oracle_text", ""),
            "cmc": data.get("cmc", 0),
            "rarity": data.get("rarity", "unknown")
        }
    return None