from fastapi import FastAPI, HTTPException, Query
from fuzzywuzzy import fuzz
from typing import List
from collections import defaultdict
from datetime import datetime
from models import VideoGame
from models import test_db

app = FastAPI()

# Copie de la DB pour ne pas l'écraser accidentellement
games_db: List[VideoGame] = test_db.copy() 

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de la base de données de jeux vidéo !"}

@app.post("/games/", response_model=VideoGame)
def create_game(game: VideoGame):
    # Vérifie si le jeu existe déjà avec la similarité fuzzy
    for existing_game in games_db:
        #if existing_game.name.lower() == game.name.lower():
        #   raise HTTPException(status_code=400, detail="Un jeu avec ce nom existe déjà.")
        similarity = fuzz.ratio(existing_game.name.lower(), game.name.lower())
        if similarity > 85:  # Seuil de tolérance, 85% de similarité
            raise HTTPException(
                status_code=400,
                detail=f"Un jeu au nom très proche existe déjà : {existing_game.name} (similarité {similarity}%)"
            )
        
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

@app.put("/games/{game_id}", response_model=VideoGame)
def update_game(game_id: int, updated_game: VideoGame):
    for index, game in enumerate(games_db):
        if game.id == game_id:
            updated_game.id = game_id  # On conserve l'ID !
            games_db[index] = updated_game
            return updated_game

    raise HTTPException(status_code=404, detail="Jeu non trouvé.")

@app.delete("/games/{game_id}")
def delete_game(game_id: int):
    for index, game in enumerate(games_db):
        if game.id == game_id:
            del games_db[index]
            return {"message": f"Le jeu avec l'id {game_id} a été supprimé avec succès."}

    raise HTTPException(status_code=404, detail="Jeu non trouvé.")

@app.get("/dashboard/")
def get_dashboard():
    now = datetime.now()
    best_games_per_year = {}
    games_by_year = defaultdict(list)
    games_by_platform = defaultdict(int)

    # Classement par année et par plateforme
    for game in games_db:
        year = game.release_date.year
        games_by_year[year].append(game)

        for platform in game.platforms:
            games_by_platform[platform] += 1

    # Meilleur jeu par année (note la plus élevée)
    for year, games in games_by_year.items():
        best_game = max(games, key=lambda g: g.ratings)
        best_games_per_year[year] = {
            "name": best_game.name,
            "ratings": best_game.ratings
        }

    # 5 Dernières sorties (tri par date décroissante)
    latest_releases = sorted(games_db, key=lambda g: g.release_date, reverse=True)[:5]

    return {
        "best_games_per_year": best_games_per_year,
        "latest_releases": [
            {
                "name": game.name,
                "release_date": game.release_date
            } for game in latest_releases
        ],
        "games_count_by_platform": games_by_platform
    }