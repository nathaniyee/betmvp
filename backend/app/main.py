from fastapi import FastAPI
from app.services.generate_bets import generate_bets

app = FastAPI()

# python -m uvicorn backend.main:app --reload

@app.get("/bets")
def get_bets():
    overs, unders, goblins, demons = generate_bets()

    return {
        "overs": overs.to_dict(orient="records"),
        "unders": unders.to_dict(orient="records"),
        "goblins": goblins.to_dict(orient="records"),
        "demons": demons.to_dict(orient="records"),
    }