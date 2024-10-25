coords_1 = (lon1, lat1)
coords_2 = (lon2, lat2)

print(geopy.distance.geodesic(coords_1, coords_2).km)