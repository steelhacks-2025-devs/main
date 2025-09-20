import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

def count_amenities_by_distance(address, amenity_type, distance_ranges):
    """
    Count amenities within different distance ranges from an address.
    
    Args:
        address: Street address to search from
        amenity_type: OSM amenity type (e.g., 'hospital', 'school', 'restaurant')
        distance_ranges: List of distances in miles (e.g., [1, 3, 5])
    
    Returns:
        Dictionary with counts for each distance range
    """
    
    # Geocode the address
    geolocator = Nominatim(user_agent="test_agent")
    location = geolocator.geocode(address)
    
    if not location:
        return f"Could not geocode address: {address}"
    print(f"Found coordinates: {location.latitude}, {location.longitude}")
    # Convert max distance to meters for Overpass query
    max_distance_miles = max(distance_ranges)
    max_distance_meters = int(max_distance_miles * 1609.34)  # miles to meters
    
    # Overpass API query
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="{amenity_type}"](around:{max_distance_meters},{location.latitude},{location.longitude});
      way["amenity"="{amenity_type}"](around:{max_distance_meters},{location.latitude},{location.longitude});
      relation["amenity"="{amenity_type}"](around:{max_distance_meters},{location.latitude},{location.longitude});
    );
    out center meta;
    """
    
    print(f"Querying for {amenity_type} within {max_distance_miles} miles...")
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code != 200:
        return f"Error querying Overpass API: {response.status_code}"
    
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
            (location.latitude, location.longitude), 
            (lat, lon)
        ).miles
        
        name = element.get('tags', {}).get('name', 'Unnamed')
        amenities_with_distances.append({
            'name': name,
            'distance_miles': distance_miles,
            'lat': lat,
            'lon': lon
        })
    
    # Count amenities within each distance range
    results = {}
    for distance in sorted(distance_ranges):
        count = sum(1 for amenity in amenities_with_distances 
                   if amenity['distance_miles'] <= distance)
        results[f"within_{distance}_miles"] = count
    
    # Also return the detailed list for reference
    results['detailed_list'] = sorted(amenities_with_distances, 
                                    key=lambda x: x['distance_miles'])
    results['total_found'] = len(amenities_with_distances)
    
    return results

for amenity in ["hospital", "transportation"]:
    print(count_amenities_by_distance("4921 Forbes Ave, Pittsburgh, PA 15213", amenity, [1, 3, 5]))