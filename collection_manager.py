import pandas as pd

def normalize_headers(df: pd.DataFrame):
    # lower-case + strip whitespace
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def summarize_collection(df: pd.DataFrame):
    df = normalize_headers(df)
    if "card name" not in df.columns or "quantity" not in df.columns:
        raise ValueError(f"Expected columns 'Quantity' and 'Card Name', got: {df.columns.tolist()}")

    total_cards = df["quantity"].sum()
    unique_cards = df["card name"].nunique()
    return {
        "total": int(total_cards),
        "unique": int(unique_cards),
    }
