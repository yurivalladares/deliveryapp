from urllib import parse
from requests import request




def get_location(query: str, first: bool = True, addressdetails: int = 1):

    q = parse.quote(query.encode('utf8'))
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={q}&addressdetails={addressdetails}"

    response = request("GET", url).json()

    if first:
        return response[0]
    return response[:6]

def get_route_distance(lat1, lon1, lat2, lon2):

    coordinates = f'{lon1},{lat1};{lon2},{lat2}'

    url = f'http://router.project-osrm.org/route/v1/driving/{coordinates}?overview=false'

    response = request("GET", url).json()

    route_distance = round(float(response['routes'][0]['distance'])/1000, 1)

    return route_distance


