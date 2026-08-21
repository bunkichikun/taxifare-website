import datetime
import requests
import time

import pandas as pd
import streamlit as st


'''
# Benoît's Incredible TaxiFareModel Frontend
'''

st.markdown("## 🕛 When do you want a ride?")

p_dt = st.datetime_input("Choose a time:", datetime.datetime.now())

st.markdown("## :color[🚀 Pickup Location]{background='#00ff0d'}")

columns = st.columns(2)
p_lat = columns[0].number_input('Pick-up Latitude', min_value=40.5 , max_value=40.9, value=40.7)
p_lon = columns[1].number_input('Pick-up Longitude', min_value=-74.7 , max_value=-73.3, value=-73.5)

st.markdown("## :color[🎯 Drop-off Location]{background='#d86060'}")
columns2 = st.columns(2)

d_lat = columns2[0].number_input('Pick-up Latitude', min_value=40.5 , max_value=40.9, value=40.8)
d_lon = columns2[1].number_input('Pick-up Longitude', min_value=-74.7 , max_value=-73.3, value=-73.6)

if st.button('Show Map!'):
    ride_df = pd.DataFrame(
        {"lat": [p_lat, d_lat],
         "lon": [p_lon, d_lon],
         "color":["#00ff0d","#d86060"]}
    )

    st.map(ride_df, size=1000, color="color")

st.markdown("## 👥 Passengers")

nb_passengers = st.slider('How many passengers', 1, 8, 2)


url = 'https://taxifare-679925498154.europe-west1.run.app/predict/'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

params = {
    "pickup_datetime" : p_dt,
    "pickup_longitude" : p_lon,
    "pickup_latitude" : p_lat,
    "dropoff_longitude" : d_lon,
    "dropoff_latitude" : d_lat,
    "passenger_count" :   nb_passengers
}

def fake_progress_bar():
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(11):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Loading')
        bar.progress(10 * i )
        time.sleep(0.05)



if st.button('GO!'):
    try:
        result = requests.get(url=url, params=params)
        pred = result.json()
        fake_progress_bar()
        st.success(f"Your ride estimated cost is: 💲{round(pred["fare"],2)}")
    except:
        st.error("Hu uh... something went wrong...")
