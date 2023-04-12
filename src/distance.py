import math

# Menghitung jarak antara dua titik menggunakan rumus Haversine dalam satuan meter
def haversine(node1, node2):
    R = 6371000 # Earth's radius in meters
    lat1_rad = math.radians(node1.x)
    lat2_rad = math.radians(node2.x)
    dLat = math.radians(node2.x - node1.x)
    dLon = math.radians(node2.y - node2.y)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    
    return round(d, 4)

# Menghitung jarak antara dua titik menggunakan rumus Euclidean
def euclidean(node1, node2):
    d = math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
    return round(d, 4)