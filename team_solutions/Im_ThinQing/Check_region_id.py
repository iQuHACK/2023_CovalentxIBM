import json
import airportsdata
import http.client

airports = airportsdata.load('IATA')

def check_region_id(Destination):
    
    city_name = airports[Destination]['city']

    conn = http.client.HTTPSConnection("hotels-com-provider.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "20f4b82842msh0a60cfb5f9bf13ep1dfe41jsnaa9a78013956",
        'X-RapidAPI-Host': "hotels-com-provider.p.rapidapi.com"
        }

    conn.request("GET", f"/v2/regions?locale=en_US&query={city_name}&domain=US", headers=headers)

    res = conn.getresponse()
    data = res.read()

    region_id = json.loads(data.decode("utf-8"))['data'][0]['gaiaId']

    return region_id


