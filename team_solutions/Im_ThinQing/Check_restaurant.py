import json
import http.client
import pandas as pd
import airportsdata

airports = airportsdata.load('IATA')

def check_restaurant(Destination):

    city_name = airports[Destination]['city']

    conn = http.client.HTTPSConnection("yelp-reviews.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "20f4b82842msh0a60cfb5f9bf13ep1dfe41jsnaa9a78013956",
        'X-RapidAPI-Host': "yelp-reviews.p.rapidapi.com"
        }

    conn.request("GET", f"/business-search?query=American&location={city_name}%2C%20MA%2C%20USA&yelp_domain=yelp.com", headers=headers)

    res = conn.getresponse()
    data = res.read()

    json_obj =  json.loads(data)
    restaurant = json_obj['data']

    name = []
    rating = []
    review_count = []
    price_range = []

    for r in restaurant:
        name.append(r['name'])
        rating.append(r['rating'])
        review_count.append(r['review_count'])
        price_range.append(r['price_range'])

    df = pd.DataFrame({'name':name,'rating':rating,'review_count':review_count,'price_range':price_range})
    return df