from fastapi import FastAPI, HTTPException, Query
from typing import List
from models import VideoGame
from models import test_db

app = FastAPI()

# Fausse base de données en mémoire
games_db: List[VideoGame] = test_db.copy() 

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de la base de données de jeux vidéo !"}

@app.post("/games/", response_model=VideoGame)
def create_game(game: VideoGame):
    # Vérifie si le jeu existe déjà exactement (on fera fuzzy plus tard)
    for existing_game in games_db:
        if existing_game.name.lower() == game.name.lower():
            raise HTTPException(status_code=400, detail="Un jeu avec ce nom existe déjà.")
        
    game.id = len(games_db) + 1
    games_db.append(game)
    return game

@app.get("/games/", response_model=List[VideoGame])
def list_games(studio: str = Query(None), platform: str = Query(None)):
    # Si pas de filtres, retourne tous les jeux
    if not studio and not platform:
        return games_db

    # Sinon filtre selon les paramètres donnés
    filtered_games = games_db
    if studio:
        filtered_games = [game for game in filtered_games if game.studio.lower() == studio.lower()]
    if platform:
        filtered_games = [game for game in filtered_games if platform in game.platforms]

    return filtered_games