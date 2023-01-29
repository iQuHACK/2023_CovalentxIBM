import json
import pandas as pd
import http.client

# parser = argparse.ArgumentParser()
# parser.add_argument('-o','--origion',type=str)
# parser.add_argument('-d','--destination',type=str)
# args = parser.parse_args()


def check_flights(origin,destination,departure_date,return_date):
    conn = http.client.HTTPSConnection("skyscanner50.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "20f4b82842msh0a60cfb5f9bf13ep1dfe41jsnaa9a78013956",
        'X-RapidAPI-Host': "skyscanner50.p.rapidapi.com"
        }

    #conn.request("GET", "/api/v1/searchFlights?origin=ORD&destination=BOS&date=2023-01-29&returnDate=2023-01-30&adults=1&cabinClass=economy&filter=price&currency=USD&countryCode=US&market=en-US", headers=headers)

    #conn.request("GET", f"/api/v1/searchFlights?origin={args.origion}&destination={args.destination}&date=2023-01-29&returnDate=2023-01-30&adults=1&cabinClass=economy&filter=price&currency=USD&countryCode=US&market=en-US", headers=headers)
    
    conn.request("GET", f"/api/v1/searchFlights?origin={origin}&destination={destination}&date={departure_date}&returnDate={return_date}&adults=1&cabinClass=economy&filter=price&currency=USD&countryCode=US&market=en-US", headers=headers)

    res = conn.getresponse()
    data = res.read()
    json_obj = json.loads(data)

    flights = json_obj['data']

    flight_price_total = []

    id_departing = []
    id_returning = []

    departure_time_departing = []
    departure_time_returning = []
    
    arrival_time_departing = []
    arrival_time_returning = []

    duration_departing = []
    duration_returning = []

    carrier_departing = []
    carrier_returning = []

    for f in flights:
        flight_price_total.append(f['price']['amount'])
        id_departing.append(f['legs'][0]['id'])
        id_returning.append(f['legs'][1]['id'])
        departure_time_departing.append(f['legs'][0]['departure'])
        departure_time_returning.append(f['legs'][1]['departure'])
        arrival_time_departing.append(f['legs'][0]['arrival'])
        arrival_time_returning.append(f['legs'][1]['arrival'])
        duration_departing.append(f['legs'][0]['duration'])
        duration_returning.append(f['legs'][1]['duration'])
        carrier_departing.append(f['legs'][0]['carriers'][0]['name'])
        carrier_returning.append(f['legs'][1]['carriers'][0]['name'])

    df = pd.DataFrame({'flight_price_total':flight_price_total,'departure_time_departing':departure_time_departing,'departure_time_returning':departure_time_returning,'duration_departing':duration_departing,'duration_returning':duration_returning,'id_departing':id_departing,'id_returning':id_returning})

    # convert time to morning / afternoon / night
    df['departing_timeperiod'] = ['Morning' if 5<int(t.split('T')[1].split(':')[0])<12 else 'Afternoon' if 12<int(t.split('T')[1].split(':')[0])<18 else 'Evening' for t in departure_time_departing]
    df['returning_timeperiod'] = ['Morning' if 5<int(t.split('T')[1].split(':')[0])<12 else 'Afternoon' if 12<int(t.split('T')[1].split(':')[0])<18 else 'Evening' for t in departure_time_returning]
    df['time_code'] = ['00' if i == 'Morning' else '01' if i == 'Afternoon' else '10' for i in df['departing_timeperiod']]
    df['airline_code'] = ['00' if i == 'American' else '01' if i == 'Delta' else '10' if i == 'United' else '11' for i in df['departing_timeperiod']]

    return df

#df.to_csv('flights_info.csv',index=False)