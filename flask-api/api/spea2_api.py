# import necessary modules
# from datetime import datetime, timedelta
# import logging
# import joblib  # For loading the scalers
import pandas as pd
import sqlite3
import tensorflow as tf
from tensorflow import keras

# connect db
conn = sqlite3.connect("flask-api/api/SeniorProject.db")
print("Database is connect successfully!")
cursor = conn.cursor()

co2 = pd.read_sql_query("SELECT * FROM estimated_co2", conn)
venue = pd.read_sql_query("SELECT * FROM venue", conn)
cost = pd.read_sql_query("SELECT * FROM cost", conn)


# modify co2 to take the latest data only
co2 = co2.drop_duplicates(subset=['Latitude', 'Longitude'], keep='last')

# Merge venue & cost on 'Latitude' and 'Longitude'
merged_data = pd.merge(venue, cost, on=['Latitude', 'Longitude'])


# Merge the result with co2_data on 'Latitude' and 'Longitude'
merged_data = pd.merge(merged_data, co2, on=['Latitude', 'Longitude'])
# Filter required columns for optimization
merged_data = merged_data[['Latitude', 'Longitude','Facility_Name_x', 'Price', 'Co2Emission']]


# Check for missing values
# print(merged_data.isna().sum())

# Drop rows with missing values
data = merged_data.dropna()
print("ok")

# Import necessary modules
from pymoo.algorithms.moo.spea2 import SPEA2
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem
import numpy as np

from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

# Define the optimization problem
class MyProblem(ElementwiseProblem):
    def __init__(self, data):
        # Get the bounds correctly
        xl = data[['Latitude', 'Longitude']].min().values # lower bound (min value of latitude and longitude)
        xu = data[['Latitude', 'Longitude']].max().values # upper bound (max value of latitude and longitude) 
        super().__init__(n_var=2, n_obj=2, n_constr=0, xl=xl, xu=xu) 
        # n_var = number of variables (latitude and longitude)
        # n_obj = number of objectives (price and co2)
        self.data = data

    def _evaluate(self, x, out, *args, **kwargs):
        # Find the closest point in the dataset
        dist = np.sqrt((self.data['Latitude'] - x[0])**2 + (self.data['Longitude'] - x[1])**2)
        idx = dist.idxmin()
        price = self.data.loc[idx, 'Price']
        co2 = self.data.loc[idx, 'Co2Emission']
        out["F"] = [price, co2]

def optimize_venues(user_location):
    # Run the SPEA2 optimization process and get the pareto front
    # SPEA2 optimization is performed first
    problem = MyProblem(data)  
    algorithm = SPEA2(pop_size=100)
    termination = get_termination("n_gen", 50)
    res = minimize(problem, algorithm, termination, seed=1, save_history=True)

    # Get the optimized results from the pareto front and pareto solutions
    pareto_front = pd.DataFrame(res.F, columns=['Price', 'Co2Emission'])
    pareto_solutions = pd.DataFrame(res.X, columns=['Latitude', 'Longitude'])
    solutions = pd.merge(pareto_solutions, pareto_front, right_index=True, left_index=True)

    # Add distance column based on user's location
    solutions['Distance'] = np.sqrt((solutions['Latitude'] - user_location[0])**2 + (solutions['Longitude'] - user_location[1])**2)

    # Sort the venues based on the distance
    sorted_solutions = solutions.sort_values(by='Distance')

    # Select the closest venues (for example, top 10)
    closest_venues = sorted_solutions.head(10)
    
    # You can convert the closest venues to a list of dictionaries for JSON response
    closest_venues_list = closest_venues.to_dict(orient='records')
    
    return closest_venues_list


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


city_coordinates = {
    "Saskatchewan Province": {"lat_min": 49.000000, "lat_max": 60.000000, "lon_min": -110.000000, "lon_max": -101.000000},
    "Prince Edward Island": {"lat_min": 45.948493, "lat_max": 47.072784, "lon_min": -64.424743, "lon_max": -62.023504},
    "Ontario": {"lat_min": 41.676555, "lat_max": 56.850102, "lon_min": -95.156227, "lon_max": -74.320860},
    "Nova Scotia": {"lat_min": 43.375111, "lat_max": 47.030530, "lon_min": -66.418161, "lon_max": -59.726333},
    "Alberta": {"lat_min": 49.000000, "lat_max": 60.000000, "lon_min": -120.000000, "lon_max": -110.000000},
    "British Columbia": {"lat_min": 48.308978, "lat_max": 60.000000, "lon_min": -139.041853, "lon_max": -114.039580},
    "Manitoba": {"lat_min": 49.000000, "lat_max": 60.000000, "lon_min": -102.000000, "lon_max": -95.000000},
    "Newfoundland and Labrador": {"lat_min": 46.559847, "lat_max": 60.000000, "lon_min": -67.800000, "lon_max": -52.616667},
    "New Brunswick": {"lat_min": 44.501873, "lat_max": 48.070121, "lon_min": -69.065808, "lon_max": -63.664500},
    "Quebec": {"lat_min": 45.000000, "lat_max": 62.583446, "lon_min": -79.762590, "lon_max": -57.100000}
}


@app.route('/spea-2', methods=['POST'])
def submit_event():
    app.logger.info(f"Form data: {request.json}")
    
    data = request.get_json()
    event_name = data.get('event-name')
    type_of_event = data.get('event-type')
    event_date = data.get('start-date')
    number_of_guests = data.get('guests')
    location_of_province = data.get('province')
    # email = data.get('Email')
    # describe_goals = data.get('Describe-Your-Goals')

    app.logger.info(f"Received event: {event_name}, Type: {type_of_event}, Date: {event_date}, "
                    f"Number of guests: {number_of_guests}, Location: {location_of_province}, "
                    #f"Email: {email}, Goals: {describe_goals}"
                    )
    
    if location_of_province not in city_coordinates:
        return jsonify({"error": "Invalid location"}), 400
    
    # Get latitude and longitude boundaries for the province
    lat_min = city_coordinates[location_of_province]['lat_min']
    lat_max = city_coordinates[location_of_province]['lat_max']
    lon_min = city_coordinates[location_of_province]['lon_min']
    lon_max = city_coordinates[location_of_province]['lon_max']
    
    user_latitude = (lat_min + lat_max) / 2
    user_longitude = (lon_min + lon_max) / 2
    user_location = [user_latitude, user_longitude]
    closest_venues = optimize_venues(user_location)
    
    print(user_location, closest_venues)

    return jsonify(status='success', message='Event submitted successfully!', venues=closest_venues)



if __name__ == '__main__':
    app.run(debug=True)