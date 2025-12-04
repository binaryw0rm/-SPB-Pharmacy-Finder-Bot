import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Вычисляет расстояние между двумя точками (в км) по формуле Haversine.
    """
    R = 6371  # Радиус Земли в км

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def get_google_maps_link(user_lat, user_lon, target_lat, target_lon):
    """Генерация ссылки на маршрут"""
    return f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={target_lat},{target_lon}&travelmode=walking"