from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd

from collection_manager import summarize_collection
from deck_suggestions import suggest_commanders, suggest_decks
from analytics import generate_analytics

app = FastAPI()

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory collection
collection = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_collection(request: Request, file: UploadFile):
    global collection
    if file.filename.endswith(".csv"):
        collection = pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        collection = pd.read_excel(file.file)
    else:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Unsupported file type"})
    
    summary = summarize_collection(collection)
    return templates.TemplateResponse("collection.html", {"request": request, "summary": summary})

@app.get("/suggest-commanders/", response_class=HTMLResponse)
async def commander_suggestions(request: Request):
    if collection is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Upload a collection first!"})
    commanders = suggest_commanders(collection)
    return templates.TemplateResponse("suggestions.html", {"request": request, "commanders": commanders})

@app.get("/suggest-decks/", response_class=HTMLResponse)
async def deck_suggestions(request: Request):
    if collection is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Upload a collection first!"})
    decks = suggest_decks(collection)
    return templates.TemplateResponse("suggestions.html", {"request": request, "decks": decks})

@app.get("/analytics/", response_class=HTMLResponse)
async def analytics(request: Request):
    if collection is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Upload a collection first!"})
    charts = generate_analytics(collection)
    return templates.TemplateResponse("analytics.html", {"request": request, "charts": charts})
