from scryfall_api import fetch_card_data
from mtggoldfish_api import fetch_commander_decklists
from collection_manager import normalize_headers

def suggest_commanders(df):
    """Find legendary creatures in the collection."""
    df = normalize_headers(df)
    commanders = []
    for _, row in df.iterrows():
        card = fetch_card_data(row["card name"])
        if card and "Legendary Creature" in card["type"]:
            commanders.append(card["name"])
    return commanders

def compare_collection_to_deck(collection_df, deck_cards):
    df = normalize_headers(collection_df)
    owned = set(df["card name"].str.lower())
    deck_set = set([c.lower() for c in deck_cards])
    overlap = owned.intersection(deck_set)
    missing = deck_set - owned
    completeness = round(len(overlap) / len(deck_set) * 100, 2) if deck_set else 0
    return completeness, list(missing)

def suggest_decks(df):
    df = normalize_headers(df)
    meta_decks = fetch_commander_decklists()
    suggestions = []
    for deck in meta_decks:
        completeness, missing = compare_collection_to_deck(df, deck["cards"])
        if completeness > 60:  # Only show decks 60%+ buildable
            suggestions.append({
                "commander": deck["name"],
                "url": deck["url"],
                "completeness": f"{completeness}%",
                "missing_cards": missing[:10]  # Limit preview
            })
    return sorted(suggestions, key=lambda x: float(x["completeness"][:-1]), reverse=True)
