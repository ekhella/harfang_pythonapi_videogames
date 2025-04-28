from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# On pourrait aussi utiliser pytest.

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API de la base de données de jeux vidéo !"}
    print(" Test Root Validé")

def test_list_games():
    response = client.get("/games/")
    assert response.status_code == 200
    games = response.json()
    assert isinstance(games, list)
    assert len(games) >= 3  # car on a mis 3 jeux dans test_db
    print(" Test Listing Validé")

def test_create_duplicate_game():
    # Essaie d'ajouter un jeu qui existe déjà (fuzzy matching)
    new_game = {
        "name": "The Witcher 3 Wild Hunt",  # très proche
        "release_date": "2015-05-19",
        "studio": "CD Projekt RED",
        "ratings": 19,
        "platforms": ["PC", "PS4"]
    }
    response = client.post("/games/", json=new_game)
    assert response.status_code == 400
    assert "proche existe déjà" in response.json()["detail"]
    print(" Test Création Validé")

def test_dashboard():
    response = client.get("/dashboard/")
    assert response.status_code == 200
    dashboard = response.json()
    assert "best_games_per_year" in dashboard
    assert "latest_releases" in dashboard
    assert "games_count_by_platform" in dashboard
    # On vérifie ici que quelque chose est renvoyé, pas que c'est correct
    print(" Test Dashboard Validé")

if __name__ == "__main__":
    test_read_root()
    test_list_games()
    test_create_duplicate_game()
    test_dashboard()
