import geopy.distance

lat1 = 18.4636219
lon1 = 73.8656288
lat2 = 18.540134
lon2 = 73.829581

coords_1 = (lon1, lat1)
coords_2 = (lon2, lat2)

print(geopy.distance.geodesic(coords_1, coords_2).km)
