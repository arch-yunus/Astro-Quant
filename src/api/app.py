import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from src.astro_engine.engine import AstroEngine
from src.analyzer.correlation import AstroAnalyzer
from src.data_ingestion.fetcher import DataFetcher
from src.analyzer.signals import ConfluenceEngine
from src.api.webhooks import router as webhook_router

app = FastAPI(title="Astro-Quant API", version="1.0.0")

# Include Routers
app.include_router(webhook_router)

# Shared Engine Components (Lazy Init in production would be better)
engine = AstroEngine()
fetcher = DataFetcher()
analyzer = AstroAnalyzer(engine)
confluence = ConfluenceEngine()

class SignalResponse(BaseModel):
    asset: str
    sentiment_score: float
    signal: str
    timestamp: datetime.datetime

@app.get("/api/v1/health")
def health_check():
    return {"status": "operational", "engine": "Swiss Ephemeris", "mode": "AOS-High-Density"}

@app.get("/api/v1/astro-state")
def get_astro_state():
    """
    Returns the current state of major planets.
    """
    now = datetime.datetime.now()
    planets = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
    state = {}
    
    for p in planets:
        data = engine.get_planetary_data(now, p)
        is_retro = engine.check_event(now, p, "Retrograde")
        state[p] = {
            "longitude": data["longitude"],
            "retrograde": is_retro,
            "speed": data["speed"]
        }
    
    return {"timestamp": now, "planetary_states": state}

@app.get("/api/v1/signals/{asset}")
def get_signal(asset: str):
    """
    Generates a live celestial trade signal for a given asset.
    """
    try:
        df = fetcher.fetch_stock(symbol=asset, period="1mo")
        df = fetcher.normalize_market_data(df)
        df_enriched = analyzer.enrich_with_astro(df, planets=["Mercury", "Venus", "Mars"])
        
        sentiment = confluence.calculate_sentiment_score(df_enriched).iloc[-1]
        raw_signal = confluence.get_signal_zones(df_enriched).iloc[-1]
        
        signal_map = {1: "LONG", -1: "SHORT", 0: "NEUTRAL"}
        
        return {
            "asset": asset,
            "sentiment_score": float(sentiment),
            "signal": signal_map.get(int(raw_signal), "NEUTRAL"),
            "timestamp": datetime.datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
