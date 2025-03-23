# ️ Projet SIG Web - GeoInnovations ️

## Description

Ce projet permet de visualiser et d'interagir avec les données géospatiales des parcs de Sherbrooke. Il offre une API RESTful  construite avec Flask  pour récupérer les informations des parcs (localisation , superficie , équipements ️) et une interface web interactive basée sur Leaflet.js ️ pour visualiser ces données sur une carte.

## Fonctionnalités

* **API RESTful ️** :
    * Récupération de la liste de tous les parcs .
    * Récupération des détails d'un parc spécifique par son ID 🆔.
    * Recherche des parcs à proximité d'une localisation donnée (latitude ⬆️, longitude ➡️) dans un rayon spécifié .
    * Calcul de la superficie totale des parcs dans un rayon donné autour d'une localisation .
* **Interface Web Interactive ️** :
    * Affichage des parcs sur une carte Leaflet.js .
    * Recherche de parcs par ID 🆔 ou par rayon .
    * Affichage des informations des parcs (nom , superficie ) dans des tableaux .
    * Coloration dynamique des polygones des parcs en fonction des recherches .

## Prérequis

* Docker  (pour la conteneurisation)
* Un navigateur web moderne 

## Installation et Exécution

1.  **Cloner le dépôt  :**

    ```bash
    git clone https://github.com/anthodesro/GMQ580_TD2.git
    cd GMQ580_TD2
    ```

2.  **Construire l'image Docker ️ :**

    ```bash
    docker build -t geoinnovations-app .
    ```

3.  **Lancer le conteneur Docker  :**

    ```bash
    docker run -p 5000:5000 geoinnovations-app
    ```

## Utilisation de l'API

L'API est accessible à `http://localhost:5000` . Voici les points de terminaison disponibles :

* **Récupérer tous les parcs  :**

    * Endpoint : `GET /parks`
    * Exemple de requête (curl) : `curl http://localhost:5000/parks`
    * Réponse : Un tableau JSON contenant les informations de tous les parcs .

* **Récupérer un parc par ID 🆔 :**

    * Endpoint : `GET /park/<id>`
    * Exemple de requête (curl) : `curl http://localhost:5000/park/123` (remplacez 123 par l'ID du parc)
    * Réponse : Un objet JSON contenant les informations du parc spécifié .

* **Rechercher les parcs par proximité  :**

    * Endpoint : `GET /parks/near?lat=<latitude>&lon=<longitude>&distance=<distance>`
    * Paramètres :
        * `lat` : Latitude de la localisation de référence ⬆️.
        * `lon` : Longitude de la localisation de référence ➡️.
        * `distance` : Rayon de recherche en mètres .
    * Exemple de requête (navigateur) : `http://localhost:5000/parks/near?lat=45.4042&lon=-71.8888&distance=500`
    * Réponse : Un tableau JSON contenant les informations des parcs trouvés dans le rayon spécifié ️.

* **Calculer la superficie totale des parcs par proximité  :**

    * Endpoint : `GET /parks/stats?lat=<latitude>&lon=<longitude>&distance=<distance>`
    * Paramètres : Identiques à la recherche par proximité .
    * Exemple de requête (curl) : `curl "http://localhost:5000/parks/stats?lat=45.4042&lon=-71.8888&distance=1000"`
    * Réponse : Un objet JSON contenant la superficie totale des parcs trouvés dans le rayon .

## Technologies Utilisées

* **Backend ⚙️ :**
    * Flask (Python ) : Framework web pour l'API RESTful .
    * Shapely (Python ) : Librairie pour la manipulation d'objets géométriques .
* **Frontend ️ :**
    * Leaflet.js ️ : Librairie JavaScript pour les cartes interactives .
* **Conteneurisation  :**
    * Docker  : Pour le déploiement simplifié .

## Tests

Vous pouvez tester l'API en utilisant des outils comme `curl` , Postman  ou votre navigateur web .

## Améliorations Possibles

* **Optimisation de l'Endpoint de Recherche par Proximité** :
    * Améliorer la précision et la cohérence des résultats de l'endpoint `GET /parks/near?lat=<latitude>&lon=<longitude>&distance=<distance>` en :
        * Utilisant des calculs de distance géodésique pour une précision accrue, en particulier sur de longues distances.
        * Implémentant des index spatiaux dans la base de données pour accélérer les requêtes de proximité.
        * Ajoutant des options de filtrage supplémentaires (par type d'équipement, par exemple) pour affiner les résultats.
        * Mettre en place des tests unitaires et d'intégration pour garantir la fiabilité de l'endpoint.

N'hésitez pas à contribuer à ce projet en proposant des améliorations ou en signalant des problèmes .
