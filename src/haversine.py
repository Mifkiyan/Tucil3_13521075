import math

from graph import Location

def haversine_distance(node1, node2):
    R = 6371000 # Earth's radius in meters
    lat1_rad = math.radians(node1.latitude)
    lat2_rad = math.radians(node2.latitude)
    dLat = math.radians(node2.latitude - node1.latitude)
    dLon = math.radians(node2.longitude - node2.longitude)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    
    return round(d, 4)

# Test Sample
# a = Location("Jl. Ganesha 11", -6.893213, 107.610664)
# b = Location("Jl. Ir. H. Juanda No.81", -6.893730, 107.612948)
# print(haversine_distance(a, b), "meters")