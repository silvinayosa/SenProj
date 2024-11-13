###############################################################
######################### Libraries ###########################
###############################################################
from flask import Flask, request, jsonify,abort
import sqlite3
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow import keras
from datetime import datetime, timedelta
import pandas as pd
import logging
import joblib
import json  
import os

# SPEA2
from pymoo.algorithms.moo.spea2 import SPEA2
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem
###############################################################



###############################################################
###################### COSRS Config ###########################
###############################################################

app = Flask(__name__)
CORS(app, origins=["http://localhost:3001"])


###############################################################
######################### Models ##############################
###############################################################

# Load the Keras models
lstm_model = keras.models.load_model('./models/lstm1.keras')
rnn_model = keras.models.load_model('./models/rnn2.keras')

# Load the saved scalers
min_max_scaler = joblib.load('./models/latitude_longitude_scaler.pkl')
co2_scaler = joblib.load('./models/co2_scaler.pkl')



###############################################################
#################### Directories & Data #######################
###############################################################
JSON_DIR = '../database/database-csv/cost-json'
CSV_DIR = '../database/database-csv/co2-csv'

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




###############################################################
#################### Functions & Classes ######################
###############################################################

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

def connect_to_db():
    conn = sqlite3.connect("../database/SeniorProject.db", check_same_thread=False)
    return conn

db_path = '../database/SeniorProject.db'  # Update the path to match your setup

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def optimize_venues(user_location):
    # connect db
    conn = connect_to_db()
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

    # get facility name from co2 data
    names = venue[['Latitude', 'Longitude', 'Facility_Name']]

    #drop duplicates and missing values
    names = names.drop_duplicates(subset=['Latitude', 'Longitude'], keep='last')
    names = names.dropna()

    print("names:",names)
    # Drop rows with missing values
    data = merged_data.dropna()
    print("ok")
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
    
    # Find the facility names for the closest venues by merging with the names dataframe, otherwise use 'No name'
    closest_venues = pd.merge(closest_venues, names, on=['Latitude', 'Longitude'], how='left')
    closest_venues['Facility_Name'] = closest_venues['Facility_Name'].fillna('No name')
    
    
    

    # You can convert the closest venues to a list of dictionaries for JSON response
    closest_venues_list = closest_venues.to_dict(orient='records')
    
    return closest_venues_list



###############################################################
######################## API ROUTES ###########################
###############################################################

@app.route('/api/datacost/<city>', methods=['GET']) 
def get_datacost(city):
    # Construct the file path for the specified city
    json_file_path = os.path.join(JSON_DIR, f'{city}_price_ranges_with_percentage.json')

    # Check if the file exists
    if not os.path.isfile(json_file_path):
        abort(404)  # Return a 404 error if the file does not exist

    # Load the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    return jsonify(data)

@app.route('/api/dataco2/<city>', methods=['GET'])
def get_dataco2(city):
    # Construct the file path for the specified city
    csv_file_path = os.path.join(CSV_DIR, f'{city}_avg_co2.csv')

    # Check if the file exists
    if not os.path.isfile(csv_file_path):
        abort(404)  # Return a 404 error if the file does not exist

    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Get the last 6 rows and convert to a list of dictionaries
    last_six = df.tail(6).to_dict(orient='records')
    
    return jsonify(last_six)

@app.route('/get_cost_by_location', methods=['GET'])
def get_cost_by_location():
    location = request.args.get('location')
    
    if location not in city_coordinates:
        return jsonify({"error": "Invalid location"}), 400
    
    
    lat_min = city_coordinates[location]['lat_min']
    lat_max = city_coordinates[location]['lat_max']
    lon_min = city_coordinates[location]['lon_min']
    lon_max = city_coordinates[location]['lon_max']
    
    conn = connect_to_db()
    cursor = conn.cursor()
    
    
    query = """
        SELECT Facility_Name, Price 
        FROM cost 
        WHERE Latitude BETWEEN ? AND ? 
        AND Longitude BETWEEN ? AND ?
    """
    
    cursor.execute(query, (lat_min, lat_max, lon_min, lon_max))
    results = cursor.fetchall()
    
    
    if results:
        return jsonify([{"Facility_Name": row[0], "Price": row[1]} for row in results])
    else:
        return jsonify({"message": "No facilities found in this location"}), 404

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request
        data = request.get_json()

        # Extract selected city and days to predict
        city_name = data.get('city_name')
        days_to_predict = int(data.get('days'))
        datetime_str = '2023-06-23' # Actual code: data.get('datetime')
        model_name = data.get('model_name')

        # Validate city and model name
        if city_name not in city_coordinates:
            return jsonify({"error": "Invalid city selected"}), 400
        if model_name not in ['LSTM', 'RNN']:
            return jsonify({"error": "Invalid model selected"}), 400

        # Get latitude and longitude for the selected city (use the center of the lat/lon range)
        lat_min = city_coordinates[city_name]['lat_min']
        lat_max = city_coordinates[city_name]['lat_max']
        lon_min = city_coordinates[city_name]['lon_min']
        lon_max = city_coordinates[city_name]['lon_max']

        # Calculate the center of the latitude and longitude range
        original_latitude = (lat_min + lat_max) / 2  # Keep the original latitude
        original_longitude = (lon_min + lon_max) / 2  # Keep the original longitude

        # Normalize the Latitude and Longitude using the loaded scaler
        latitude, longitude = min_max_scaler.transform([[original_latitude, original_longitude]])[0]

        # Convert Start Date to a datetime object
        start_date = datetime.strptime(datetime_str, "%Y-%m-%d")

        predictions = []

        # Connect to the database
        conn = connect_to_db()
        cursor = conn.cursor()

        for i in range(days_to_predict):
            # Calculate the date for the prediction
            current_date = start_date + timedelta(days=i)
            day_of_year = current_date.timetuple().tm_yday

            # Cyclical transformation for date
            date_sin = np.sin(2 * np.pi * day_of_year / 365.25)
            date_cos = np.cos(2 * np.pi * day_of_year / 365.25)

            # Combine features into a single array
            features = np.array([[latitude, longitude, date_sin, date_cos]])

            # Reshape the input data to match the model's input shape
            features_array = features.reshape((features.shape[0], 1, features.shape[1]))

            # Choose the correct model for prediction
            if model_name == 'LSTM':
                prediction = lstm_model.predict(features_array)
            else:  # model_name == 'RNN'
                prediction = rnn_model.predict(features_array)

            # Perform inverse normalization on the predicted CO2 value
            co2_emission_scaled = float(prediction[0][0])
            co2_emission = co2_scaler.inverse_transform([[co2_emission_scaled]])[0][0]

            # Append the prediction for the current date
            predictions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "CO2Emission": co2_emission
            })

            # Insert the prediction into the 'co2' table using the original latitude and longitude
            # cursor.execute("""
            #     INSERT INTO estimated_co2 (Latitude, Longitude, DateTime, Co2Emission) 
            #     VALUES (?, ?, ?, ?)
            # """, (original_latitude, original_longitude, current_date.strftime("%Y-%m-%d"), co2_emission))
        
        # # Commit the transaction and close the connection
        # conn.commit()
        # conn.close()

        # Return predictions for all requested days
        return jsonify({"predictions": predictions})

    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    
    conn = get_db_connection()
    
    query = 'SELECT Event_name, Start_date, Description, Picture, RegistrationPrice FROM user_event WHERE OpentoPublic = 1'
    events = conn.execute(query).fetchall()
    conn.close()
    
    # Convert rows to dictionaries
    event_list = [dict(row) for row in events]
    return jsonify(event_list)

logging.basicConfig(level=logging.INFO)

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
    
    print( closest_venues)

    return jsonify(closest_venues)


###############################################################
#################### connect to DB ############################
###############################################################
# def connect_to_db():
#     conn = sqlite3.connect('SeniorProject.db')
#     return conn

###############################################################
#################### Login api ################################
###############################################################

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('Email')
    password = data.get('Password')

    conn = connect_to_db()
    print("Database is connect successfully!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE Email = ? AND Password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Incorrect Email or Password"}), 401



###############################################################
#################### Main Port:5000 ###########################
###############################################################
if __name__ == '__main__':
    app.run(debug=True)


# CO2 prediction api :(POST) http://127.0.0.1:5000/predict
# Cost location api :(GET) http://127.0.0.1:5000/get_cost_by_location?location=Ontario
# Get user input event form data : (POST) http://127.0.0.1:5000/submit_event
