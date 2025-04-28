# Utilise une image légère officielle Python
FROM python:3.11-slim

# Crée (si nécessaire) le dossier de travail /app dans le conteneur.
WORKDIR /app

# Se fait dans /app :
# Copier les fichiers requirements et installe les dépendances
COPY requirements.txt .
# requirements définis avec : pip freeze > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet dans le conteneur
COPY . .

EXPOSE 8000

# Lancer Uvicorn quand le conteneur démarre
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
