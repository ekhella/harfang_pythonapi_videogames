from fastapi import FastAPI, HTTPException
from typing import List
from models import VideoGame

app = FastAPI()

# Fausse base de données en mémoire
games_db: List[VideoGame] = []

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de la base de données de jeux vidéo !"}

@app.post("/games/", response_model=VideoGame)
def create_game(game: VideoGame):
    # Vérifie si le jeu existe déjà exactement (on fera fuzzy plus tard)
    for existing_game in games_db:
        if existing_game.name.lower() == game.name.lower():
            raise HTTPException(status_code=400, detail="Un jeu avec ce nom existe déjà.")

    games_db.append(game)
    return game
