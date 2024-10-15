from urllib.parse import urlparse, parse_qs

# Example Google Maps URL
url = 'https://www.google.co.in/maps/place/Kumar+Palmcrest/@18.4478097,73.8969951,17z/data=!3m1!4b1!4m6!3m5!1s0x3bc2ea518af97b83:0x5ebf06474f904d15!8m2!3d18.4478097!4d73.89957!16s%2Fg%2F11cn3sg86d?entry=ttu&g_ep=EgoyMDI0MTAwOS4wIKXMDSoASAFQAw%3D%3D'

# Parse the URL
parsed_url = urlparse(url)

# Extract the part after @ which contains the coordinates
if '@' in parsed_url.path:
    path_parts = parsed_url.path.split('@')[1].split(',')
    latitude = path_parts[0]
    longitude = path_parts[1]
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Coordinates not found in the URL.")