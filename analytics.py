import matplotlib.pyplot as plt
import pandas as pd
import os
from scryfall_api import fetch_card_data
from collection_manager import normalize_headers

CHART_DIR = "static/charts"
os.makedirs(CHART_DIR, exist_ok=True)

def generate_color_pie(df):
    df = normalize_headers(df)
    colors = []
    for _, row in df.iterrows():
        card = fetch_card_data(row["card name"])
        if card:
            colors.extend(card["colors"] or ["Colorless"])
    color_counts = pd.Series(colors).value_counts()
    fig, ax = plt.subplots()
    color_counts.plot.pie(ax=ax, autopct='%1.1f%%')
    ax.set_ylabel("")
    path = os.path.join(CHART_DIR, "color_pie.png")
    plt.savefig(path)
    plt.close()
    return "/static/charts/color_pie.png"

def generate_type_distribution(df):
    df = normalize_headers(df)
    types = []
    for _, row in df.iterrows():
        card = fetch_card_data(row["card name"])
        if card:
            main_type = card["type"].split("—")[0].strip()
            types.append(main_type)
    type_counts = pd.Series(types).value_counts()
    fig, ax = plt.subplots()
    type_counts.plot.bar(ax=ax)
    ax.set_ylabel("Count")
    ax.set_xlabel("Card Type")
    path = os.path.join(CHART_DIR, "type_distribution.png")
    plt.savefig(path)
    plt.close()
    return "/static/charts/type_distribution.png"

def generate_mana_curve(df):
    df = normalize_headers(df)
    cmcs = []
    for _, row in df.iterrows():
        card = fetch_card_data(row["card name"])
        if card:
            cmcs.append(int(card["cmc"]))
    series = pd.Series(cmcs).value_counts().sort_index()
    fig, ax = plt.subplots()
    series.plot.bar(ax=ax)
    ax.set_xlabel("Converted Mana Cost (CMC)")
    ax.set_ylabel("Number of Cards")
    path = os.path.join(CHART_DIR, "mana_curve.png")
    plt.savefig(path)
    plt.close()
    return "/static/charts/mana_curve.png"

def generate_analytics(df):
    return {
        "color_pie": generate_color_pie(df),
        "type_dist": generate_type_distribution(df),
        "mana_curve": generate_mana_curve(df)
    }
