import json
import pandas as pd
import http.client

def check_hotel(region_id,Departure_date,Return_date):
    conn = http.client.HTTPSConnection("hotels-com-provider.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "20f4b82842msh0a60cfb5f9bf13ep1dfe41jsnaa9a78013956",
        'X-RapidAPI-Host': "hotels-com-provider.p.rapidapi.com"
        }

    conn.request("GET", f"/v2/hotels/search?domain=US&sort_order=PRICE_LOW_TO_HIGH&locale=en_US&checkout_date={Return_date}&region_id={region_id}&adults_number=1&checkin_date={Departure_date}&available_filter=SHOW_AVAILABLE_ONLY&meal_plan=FREE_BREAKFAST&guest_rating_min=8&price_min=10&page_number=1&amenities=WIFI%2CPARKING&price_max=500&lodging_type=HOTEL%2CHOSTEL%2CAPART_HOTEL&star_rating_ids=3%2C4%2C5", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # parse 

    json_obj = json.loads(data)

    with open('hotel_info.json', 'w') as outfile:
        json.dump(json_obj, outfile,indent=4)

    hotels = json_obj['properties']

    names = []
    prices = []
    review_score = []
    review_count = []
    star = []

    for h in hotels:
        names.append(h['name'])
        prices.append(h['price']['lead']['formatted'])
        review_score.append(h['reviews']['score'])
        review_count.append(h['reviews']['total'])
        star.append(h['star'])

    df = pd.DataFrame({'name':names,'price':prices,'review_score':review_score,'review_count':review_count,'star':star})
    return df