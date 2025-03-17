import geopandas as gpd
from flask import Flask, jsonify, request
from shapely.geometry import Point
from shapely.ops import transform
import pyproj

# Initialisation de l'application Flask
app = Flask(__name__)

# Charger les données géospatiales depuis le fichier GeoJSON
gdf_parks = gpd.read_file('data/AireAmenagee.geojson')

# Définir le système de coordonnées de référence (CRS) à utiliser
gdf_parks = gdf_parks.to_crs(epsg=4326)  # CRS WGS84 pour la latitude et longitude

# Endpoint pour récupérer la liste de tous les parcs
@app.route('/parks', methods=['GET'])
def get_parks():
    parks_list = gdf_parks[['nom', 'superficie', 'geometry']].to_dict(orient='records')
    return jsonify(parks_list)

# Endpoint pour récupérer les détails d'un parc spécifique en fonction de son id
@app.route('/park/<int:id>', methods=['GET'])
def get_park(id):
    park = gdf_parks.iloc[id]
    park_details = {
        'nom': park['nom'],
        'superficie': park['superficie'],
        'geometry': park['geometry'].__geo_interface__
    }
    return jsonify(park_details)

# Endpoint pour récupérer les parcs dans un rayon donné autour d'une position
@app.route('/parks/near', methods=['GET'])
def get_parks_near():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    distance = float(request.args.get('distance'))  # en mètres

    # Créer un point à partir des coordonnées de l'utilisateur
    user_point = Point(lon, lat)

    # Créer un buffer autour du point utilisateur pour définir la zone de recherche
    buffer = user_point.buffer(distance)

    # Filtrer les parcs à l'intérieur de cette zone
    parks_in_radius = gdf_parks[gdf_parks.intersects(buffer)]

    parks_list = parks_in_radius[['nom', 'superficie', 'geometry']].to_dict(orient='records')
    return jsonify(parks_list)

# Endpoint pour récupérer la superficie des parcs dans un rayon donné autour d'une position
@app.route('/parks/stats', methods=['GET'])
def get_parks_stats():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    distance = float(request.args.get('distance'))  # en mètres

    # Créer un point à partir des coordonnées de l'utilisateur
    user_point = Point(lon, lat)

    # Créer un buffer autour du point utilisateur pour définir la zone de recherche
    buffer = user_point.buffer(distance)

    # Filtrer les parcs à l'intérieur de cette zone
    parks_in_radius = gdf_parks[gdf_parks.intersects(buffer)]

    # Calculer la superficie totale des parcs dans cette zone
    total_area = parks_in_radius['superficie'].sum()
    return jsonify({'superficie_totale': total_area})

if __name__ == '__main__':
    app.run(debug=True)
