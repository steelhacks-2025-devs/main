import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import pandas as pd
import os
import math

def count_amenities_by_distance(zip_lat, zip_lon, amenity_type, distance_ranges):
    """
    Count amenities within different distance ranges from an address.
    
    Args:
        lat: Latitude of the address
        lon: Longitude of the address
        amenity_type: OSM amenity type (e.g., 'hospital', 'school', 'restaurant')
        distance_ranges: List of distances in miles (e.g., [1, 3, 5])
    
    Returns:
        Dictionary with counts for each distance range
    """

    # Convert max distance to meters for Overpass query
    max_distance_miles = max(distance_ranges)
    max_distance_meters = int(max_distance_miles * 1609.34)  # miles to meters
    
    # Overpass API query
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["amenity"~"^({amenity_type})"](around:{max_distance_meters},{zip_lat},{zip_lon});
      way["amenity"~"^({amenity_type})"](around:{max_distance_meters},{zip_lat},{zip_lon});
      relation["amenity"~"^({amenity_type})"](around:{max_distance_meters},{zip_lat},{zip_lon});
    );
    out center meta;
    """
    
    print(f"Querying for {amenity_type} within {max_distance_miles} miles of {zip_lat}, {zip_lon}...")
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code != 200:
        print("Error querying Overpass API for coordinate: {zip_lat}, {zip_lon}: {response.status_code}")
        return None
    
    data = response.json()
    
    # Calculate distances and count by ranges
    amenities_with_distances = []
    
    for element in data['elements']:
        # Get coordinates (different for nodes vs ways/relations)
        if element['type'] == 'node':
            lat, lon = element['lat'], element['lon']
        elif 'center' in element:
            lat, lon = element['center']['lat'], element['center']['lon']
        else:
            continue
        
        # Calculate distance in miles
        distance_miles = geodesic(
            (zip_lat, zip_lon), 
            (lat, lon)
        ).miles
        
        name = element.get('tags', {}).get('name', 'Unnamed')
        if name == 'Unnamed':
            continue
        amenities_with_distances.append({
            'name': name,
            'distance_miles': distance_miles,
            'lat': lat,
            'lon': lon
        })
    
    # Count amenities within each distance range
    results = {'within_1_mi': 0, 'within_3_mi': 0, 'within_5_mi': 0}

    for amenity in amenities_with_distances:
        distance = amenity['distance_miles']
        if distance <= 1:
            results['within_1_mi'] += 1
        elif 1 < distance <= 3:
            results['within_3_mi'] += 1
        elif 3 < distance <= 5:
            results['within_5_mi'] += 1
    
    # Also return the detailed list for reference
    results['detailed_list'] = sorted(amenities_with_distances, 
                                    key=lambda x: x['distance_miles'])
    results['total_found'] = len(amenities_with_distances)
    
    return results

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, 'datasets', 'finalpt6.csv')
df = pd.read_csv(csv_file)
# Extract LAT and LON tuples from the dataframe
coordinates = list(set(zip(df['LAT'], df['LON'])))
print(len(coordinates))
print(f"testing {len(coordinates)} zipcode centroids...")

amenity_types = {
    "medical": "hospital|clinic|pharmacy|emergency care|health center|urgent care|physical therapy",
    # "transportation": "bus station|pittsburgh regional transit|transit station|train station|subway station|metro station|errand service|taxi|bus stop",
    "grocery": "grocery store|supermarket|market|drugstore",
    "recreation": "park|rec center|community center|pool|gym|fitness center",
    "entertainment": "movie theater|theater|concert hall|museum|art gallery|zoo|aquarium|library|bookstore|record store|music venue|comedy club|sports venue|arena",
}

print("Starting proximity scoring...")
start_time = time.time()

final_data = []

for i, coordinate in enumerate(coordinates):

    final_data.append({})
    lat, lon = coordinate
    final_data[i]["LAT"] = lat
    final_data[i]["LON"] = lon

    for category in amenity_types.keys():
        res = count_amenities_by_distance(lat, lon, amenity_types[category], [1, 3, 5])
        if res is None:
            print(f"Error querying Overpass API for coordinate: {lat}, {lon} and category: {category}")
            continue
        # Calculate distance-weighted proximity index using inverse distance weighting
        proximity_index = 0
        detailed_list = res['detailed_list']
        
        if len(detailed_list) > 0:
            # Use gentler proximity weighting with diminishing returns
            # 1/(1+distance) gives extra weight to close proximity without being too aggressive
            proximity_weights = sum(1 / (1 + amenity['distance_miles']) for amenity in detailed_list)
            
            # Use tanh for natural diminishing returns and cap at 100
            count_factor = math.tanh(len(detailed_list) / 30) * 65  # Scales count influence
            proximity_factor = math.tanh(proximity_weights / 30) * 35  # Scales proximity influence
            
            proximity_index = min(100, proximity_factor + count_factor)
        
        print(f"{category.capitalize()} total found: {res['total_found']}")
        print(f"{category.capitalize()} within 1 mi: {res['within_1_mi']}")
        print(f"{category.capitalize()} within 1-3 mi: {res['within_3_mi']}")
        print(f"{category.capitalize()} within 1-5 mi: {res['within_5_mi']}")
        print(f"{category.capitalize()} proximity index: {proximity_index}")
        final_data[i][f"{category}_prox_score"] = proximity_index
    
df = pd.DataFrame(final_data)
df.to_csv(os.path.join(BASE_DIR, 'datasets', 'zipcode_centroid_proximity_scores.csv'), index=False)
end_time = time.time()
print("Done!")
print(f"Time taken: {end_time - start_time} seconds")