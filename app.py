from flask import Flask, jsonify, request, render_template
from shapely.geometry import shape, Point
import pyproj
import json

app = Flask(__name__)

try:
    with open('data/AireAmenagee.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    print("✅ Données chargées avec succès.")

    parks = []
    crs_4326 = pyproj.CRS.from_epsg(4326)
    crs_3857 = pyproj.CRS.from_epsg(3857)
    transformer_4326_to_3857 = pyproj.Transformer.from_crs(crs_4326, crs_3857, always_xy=True)
    transformer_3857_to_4326 = pyproj.Transformer.from_crs(crs_3857, crs_4326, always_xy=True)

    for feature in geojson_data['features']:
        try:
            geometry = shape(feature['geometry'])

            if geometry.geom_type == 'Point':
                geometry_3857 = Point(transformer_4326_to_3857.transform(geometry.x, geometry.y))
            elif geometry.geom_type == 'Polygon':
                coords_3857 = [
                    transformer_4326_to_3857.transform(x, y) for x, y in geometry.exterior.coords
                ]
                geometry_3857 = shape({'type': 'Polygon', 'coordinates': [coords_3857]})

            else:
                geometry_3857 = geometry

            superficie = round(geometry_3857.area / 1e6, 2) if geometry_3857.geom_type == 'Polygon' else 0

            parks.append({
                'id': feature['id'],
                'NOM': feature['properties']['NOM'],
                'geometry_3857': geometry_3857,
                'superficie': superficie
            })
        except Exception as e:
            print(f"❌ Erreur lors du traitement de la feature {feature['id']}: {e}")

except Exception as e:
    print(f"❌ Erreur lors du chargement ou du traitement des données : {e}")
    parks = []

def validate_coords(lat, lon, distance):
    """Valide les coordonnées et la distance."""
    try:
        lat, lon, distance = float(lat), float(lon), float(distance)
        if not (-90 <= lat <= 90 and -180 <= lon <= 180 and distance > 0):
            raise ValueError("Valeurs de coordonnées invalides.")
        return lat, lon, distance
    except (TypeError, ValueError):
        return None

@app.route('/')
def index():
    return render_template('base.html', title="Accueil")

@app.route('/parks', methods=['GET'])
def get_parks():
    if not geojson_data:
        return jsonify({'error': 'Données non disponibles'}), 500

    parks_list = []
    for park in parks:
        # Conversion de la géométrie en EPSG:4326
        park_geometry_4326 = park['geometry_3857']
        if park_geometry_4326.geom_type == 'Polygon':
            coords_4326 = [
                transformer_3857_to_4326.transform(x, y) for x, y in park_geometry_4326.exterior.coords
            ]
            park_geometry_4326 = {'type': 'Polygon', 'coordinates': [coords_4326]}
        elif park_geometry_4326.geom_type == 'Point':
            x, y = transformer_3857_to_4326.transform(park_geometry_4326.x, park_geometry_4326.y)
            park_geometry_4326 = {'type': 'Point', 'coordinates': [x, y]}

        parks_list.append({
            'id': park['id'],
            'NOM': park['NOM'],
            'superficie': park['superficie'],
            'geometry': park_geometry_4326 if isinstance(park_geometry_4326, dict) else park_geometry_4326.__geo_interface__
        })

    return jsonify(parks_list)

@app.route('/park/<int:id>', methods=['GET'])
def get_park(id):
    """Retourne les détails d'un parc spécifique en fonction de son id."""
    if not geojson_data:
        return jsonify({'error': 'Données non disponibles'}), 500

    park = next((p for p in parks if p['id'] == id), None)
    if not park:
        return jsonify({'error': 'Parc non trouvé'}), 404

    return jsonify({
        'id': park['id'],
        'NOM': park['NOM'],
        'superficie': park['superficie'],
        'geometry': park['geometry_3857'] if isinstance(park['geometry_3857'], dict) else park['geometry_3857'].__geo_interface__
    })

@app.route('/parks/near', methods=['GET'])
def get_parks_near():
    """Retourne les parcs à proximité d'un point donné."""
    lat, lon, distance = request.args.get('lat'), request.args.get('lon'), request.args.get('distance')

    coords = validate_coords(lat, lon, distance)
    if not coords:
        return jsonify({'error': 'Coordonnées invalides'}), 400

    lat, lon, distance = coords

    # Transformer le point utilisateur en Web Mercator
    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    user_point = Point(transformer.transform(lon, lat))

    # Créer un polygone circulaire (buffer) autour du point utilisateur
    user_buffer = user_point.buffer(distance)

    if not geojson_data:
        return jsonify({'error': 'Données non disponibles'}), 500

    parks_in_radius = []
    for park in parks:
        park_geometry = park['geometry_3857']

        # Vérifier directement si le polygone du parc intersecte le buffer
        if park_geometry.intersects(user_buffer):
            # Calculer l'intersection
            intersection = park_geometry.intersection(user_buffer)

            if not intersection.is_empty:
                # Calculer le pourcentage de recouvrement
                park_area = park_geometry.area
                if park_area > 0:
                    overlap_percentage = intersection.area / park_area
                else:
                    overlap_percentage = 1.0  # Si le parc n'a pas d'aire définie, considérer comme inclus

                # Ajuster le seuil pour détecter plus de parcs (ex: > 0.1 pour 10% au lieu de 50%)
                if overlap_percentage > 0.05:
                    parks_in_radius.append(park)

    parks_list = [
        {
            'id': park['id'],
            'NOM': park['NOM'],
            'superficie': park['superficie'],
            'geometry': park['geometry_3857'] if isinstance(park['geometry_3857'], dict) else park['geometry_3857'].__geo_interface__
        }
        for park in parks_in_radius
    ]

    return jsonify(parks_list)

@app.route('/parks/stats', methods=['GET'])
def get_parks_stats():
    """Retourne la superficie totale des parcs dans un rayon donné."""
    lat, lon, distance = request.args.get('lat'), request.args.get('lon'), request.args.get('distance')

    coords = validate_coords(lat, lon, distance)
    if not coords:
        return jsonify({'error': 'Coordonnées invalides'}), 400

    lat, lon, distance = coords

    # Transformer le point utilisateur en Web Mercator
    transformer = pyproj.Transformer.from_crs(crs_4326, crs_3857, always_xy=True)
    user_point = Point(transformer.transform(lon, lat))
    user_buffer = user_point.buffer(distance)

    if not geojson_data:
        return jsonify({'error': 'Données non disponibles'}), 500

    parks_in_radius = [park for park in parks if park['geometry_3857'].intersects(user_buffer)]

    total_area = sum(park['superficie'] for park in parks_in_radius)

    return jsonify({'superficie_totale': round(total_area, 2)})

if __name__ == '__main__':
    app.run(debug=True)