FROM python:3.11-slim

WORKDIR /app

# Copie des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Lancement automatique : attente de PostgreSQL, création des tables, insertion des données, lancement de l'API
CMD ["sh", "-c", "python wait_for_db.py && python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]

