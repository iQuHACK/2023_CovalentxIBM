import random

import sys,os
sys.path.append(os.getcwd())

from Check_flights import check_flights
from Check_region_id import check_region_id
from Check_hotel import check_hotel
from Check_restaurant import check_restaurant
from covalent_grover_sampler import grover_function
from flask import Flask, render_template, request

app = Flask(__name__) # Creating our Flask Instance

@app.route('/', methods=['GET'])
def index():
    """ Displays the home page accessible at '/' """

    return render_template('homepage.html')

@app.route('/taskbar/', methods=['GET'])
def taskbar():
    return render_template('taskbar.html')

@app.route('/result/', methods=['POST'])
def result():
    Origin = request.form['Origin']  
    Destination = request.form['Destination']
    Departure_date = request.form['Departure_date']
    Return_date = request.form['Return_date']
    Travel_time = request.form['Travel_time']
    Airlines = request.form['Airlines']
    Food_type = request.form['Food_type']
    Price_range = request.form['Price_range']

    df_flights = check_flights(Origin,Destination,Departure_date,Return_date)
    lowest_flight_price = list(df_flights.flight_price_total)[0]
    cheapest_flight_id_departing = list(df_flights.id_departing)[0]
    cheapest_flight_id_returning = list(df_flights.id_returning)[0]

    
    region_id = check_region_id(Destination)
    df_hotel = check_hotel(region_id,Departure_date,Return_date)
    flight_time_code_dict = {list(df_flights.time_code)[i]: list(df_flights.flight_price_total)[i] for i in range(len(df_flights))}
    flight_airline_code_dict = {list(df_flights.airline_code)[i]: list(df_flights.flight_price_total)[i] for i in range(len(df_flights))}
    lowest_hotel_price = list(df_hotel.price)[0]
    cheapest_hotel_name = list(df_hotel.name)[0]

    df_restaurant = check_restaurant(Destination)
    lowest_restaurant_price = list(df_restaurant.price_range)[0]
    cheapest_restaurant_name = list(df_restaurant.name)[0]

    return render_template(
            'taskbar.html',
            Origin=Origin,
            Destination=Destination,
            Departure_date=Departure_date,
            Return_date=Return_date,
            Travel_time=Travel_time,
            Airlines=Airlines,
            Food_type=Food_type,
            Price_range=Price_range,
            lowest_flight_price=lowest_flight_price,
            cheapest_flight_id_departing=cheapest_flight_id_departing,
            cheapest_flight_id_returning=cheapest_flight_id_returning,
            lowest_hotel_price=lowest_hotel_price,
            cheapest_hotel_name=cheapest_hotel_name,
            lowest_restaurant_price=lowest_restaurant_price,
            cheapest_restaurant_name=cheapest_restaurant_name,
            grover_result=grover_function("1100")
        )
    

if __name__ == '__main__':
    port = 5000 + random.randint(0, 999)
    url = f"http://127.0.0.1:{port}"
    app.run(use_reloader=False, debug=True, port=port)