# Projet SIG Web - GeoInnovations

## Description
Ce projet permet de consulter des données géospatiales sur les parcs de Sherbrooke, incluant des informations comme la localisation, la superficie et les équipements disponibles. L'API Flask expose plusieurs endpoints pour interroger ces données, et une carte Leaflet est utilisée pour visualiser les résultats.

## Instructions

### Construction et lancement du conteneur Docker
1. Clonez ce projet.
2. Créez l'image Docker :
    ```bash
    docker build -t sig-web-app .
    ```
3. Lancez le conteneur Docker :
    ```bash
    docker run -p 5000:5000 sig-web-app
    ```

### Accès à l'API
L'API sera accessible à `http://localhost:5000`.

Voici quelques exemples d'endpoints :
- **GET /parks** : Retourne tous les parcs.
- **GET /park/<id>** : Retourne un parc spécifique par son ID.
- **GET /parks/near?lat=<latitude>&lon=<longitude>&distance=<distance>** : Recherche des parcs à proximité d'une position donnée.
- **GET /parks/stats?lat=<latitude>&lon=<longitude>&distance=<distance>** : Retourne la superficie totale des parcs à proximité.

### Testing
Utilisez un navigateur ou `curl` pour tester l'API. Vous pouvez également utiliser l'interface Web fournie pour tester les recherches de parcs proches.

## Technologies
- Flask
- GeoPandas
- Shapely
- Docker
