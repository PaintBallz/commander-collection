from scryfall_api import fetch_card_data
from mtggoldfish_api import fetch_commander_decklists
from collection_manager import normalize_headers

def suggest_commanders(df):
    """Find legendary creatures in the collection, excluding Battles."""
    df = normalize_headers(df)
    commanders = []
    for _, row in df.iterrows():
        card = fetch_card_data(row["card name"])
        if card:
            type_line = card["type"]
            # Must be a Legendary Creature
            if "Legendary Creature" in type_line and "Battle" not in type_line:
                commanders.append(card["name"])
    return commanders

def compare_collection_to_deck(collection_df, deck_cards):
    df = normalize_headers(collection_df)

    # Normalize collection into dict {card_name: quantity}
    owned = (
        df.groupby("card name")["quantity"]
        .sum()
        .to_dict()
    )

    # Normalize deck into dict {card_name: quantity}
    deck_dict = {}
    for card in deck_cards:
        deck_dict[card] = deck_dict.get(card, 0) + 1

    overlap = 0
    missing = {}

    for card, need_qty in deck_dict.items():
        have_qty = owned.get(card.lower(), 0)
        if have_qty >= need_qty:
            overlap += need_qty
        else:
            overlap += have_qty
            missing[card] = need_qty - have_qty

    completeness = round(overlap / sum(deck_dict.values()) * 100, 2)
    return completeness, list(missing.keys())

def suggest_decks(df):
    """Suggest meta decks from MTGGoldfish that align with collection."""
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
                "missing_cards": missing[:10],  # preview only
                "full_list": deck["cards"],     # store full decklist
            })
    return sorted(suggestions, key=lambda x: float(x["completeness"][:-1]), reverse=True)

def format_deck_as_txt(deck):
    """Format a decklist into a plain-text export (Arena style)."""
    lines = []
    for card in deck:
        # Assume 1 copy of each card (commander decks are singleton except basics)
        lines.append(f"1 {card}")
    return "\n".join(lines)
