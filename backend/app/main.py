from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.generate_bets import generate_bets
from time import time

# python -m uvicorn backend.main:app --reload

app = FastAPI()

cached_bets = None
last_updated = 0
CACHE_TTL = 86400 # seconds -> 1 day

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/bets")
def get_bets():
    global cached_bets, last_updated

    now = time()

    # recompute if cache expired or empty
    if cached_bets is None or now - last_updated > CACHE_TTL:
        print("Recomputing bets...")

        overs, unders, goblins, demons = generate_bets()

        cached_bets = {
            "overs": overs.to_dict(orient="records"),
            "unders": unders.to_dict(orient="records"),
            "goblins": goblins.to_dict(orient="records"),
            "demons": demons.to_dict(orient="records"),
        }

        last_updated = now

    return cached_bets


@app.post("/refresh")
def refresh_bets():
    global cached_bets, last_updated

    overs, unders, goblins, demons = generate_bets()

    cached_bets = {
        "overs": overs.to_dict(orient="records"),
        "unders": unders.to_dict(orient="records"),
        "goblins": goblins.to_dict(orient="records"),
        "demons": demons.to_dict(orient="records"),
    }

    last_updated = time()

    return {"status": "refreshed"}
