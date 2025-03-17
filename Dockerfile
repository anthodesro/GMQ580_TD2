FROM python:3.12.7-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libgeos-dev \
    libproj-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de votre application dans l'image Docker
COPY . /app

# Installer les dépendances Python spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000 pour que l'application Flask soit accessible
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python", "app.py"]
