from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd

from collection_manager import summarize_collection, normalize_headers
from deck_suggestions import suggest_commanders, suggest_decks, format_deck_as_txt
from analytics import generate_analytics

app = FastAPI()

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory storage
collection = None
last_decks = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_collection(request: Request, file: UploadFile):
    global collection
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Unsupported file type"})

    # Normalize headers once
    collection = normalize_headers(df)

    summary = summarize_collection(collection)
    return templates.TemplateResponse("collection.html", {"request": request, "summary": summary})

@app.get("/clear-collection/")
async def clear_collection():
    """Clear the uploaded collection and reset state."""
    global collection, last_decks
    collection = None
    last_decks = []
    return RedirectResponse(url="/", status_code=303)

@app.get("/suggest-commanders/", response_class=HTMLResponse)
async def commander_suggestions(request: Request):
    if collection is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Upload a collection first!"})
    commanders = suggest_commanders(collection)
    return templates.TemplateResponse("suggestions.html", {"request": request, "commanders": commanders})

@app.get("/suggest-decks/", response_class=HTMLResponse)
async def deck_suggestions(request: Request):
    global last_decks
    if collection is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Upload a collection first!"})
    decks = suggest_decks(collection)
    last_decks = decks
    return templates.TemplateResponse("suggestions.html", {"request": request, "decks": decks})

@app.get("/export-deck/{deck_index}", response_class=PlainTextResponse)
async def export_deck(deck_index: int):
    if deck_index < 0 or deck_index >= len(last_decks):
        return PlainTextResponse("Invalid deck index", status_code=400)
    deck = last_decks[deck_index]
    txt = format_deck_as_txt(deck)
    filename = deck["commander"].replace(" ", "_") + ".txt"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return PlainTextResponse(txt, headers=headers)

@app.get("/analytics/", response_class=HTMLResponse)
async def analytics(request: Request):
    if collection is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Upload a collection first!"})
    charts = generate_analytics(collection)
    return templates.TemplateResponse("analytics.html", {"request": request, "charts": charts})
