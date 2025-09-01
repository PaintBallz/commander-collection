import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.mtggoldfish.com"

def fetch_commander_decklists(format="commander"):
    """Fetch commander deck archetypes from MTGGoldfish meta page."""
    url = f"{BASE_URL}/metagame/{format}/full"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    decks = []

    if resp.status_code != 200:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    deck_links = soup.select("a.deck-price-paper")

    for link in deck_links[:10]:  # Limit to first 10 archetypes
        deck_url = BASE_URL + link["href"]
        deck_name = link.get_text(strip=True)
        deck_cards = fetch_decklist(deck_url)
        decks.append({"name": deck_name, "url": deck_url, "cards": deck_cards})
    return decks

def fetch_decklist(url):
    """Scrape a decklist given its MTGGoldfish URL."""
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    card_elems = soup.select("span.deck-col-card a")
    cards = [c.get_text(strip=True) for c in card_elems]
    return cards
