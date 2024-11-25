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
import re
import secrets
import jwt
from functools import wraps


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
CORS(app, resources={r"/*": {"origins": "*"}})


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
CSV_DIR_MK = '../database/database-csv/co2-predict'

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

event_type_mapping = {
    "playground": ["Parties"],
    "pool": ["Parties", "Fundraisers", "Convention"],
    "trail": ["Fundraisers", "Convention"],
    "park": ["Parties", "Weddings", "Fundraisers", "Convention"],
    "community centre": ["Corporate Events", "Parties", "Seminars", "Weddings", "Fundraisers", "Convention"],
    "gym": ["Corporate Events", "Parties", "Convention"],
    "athletic park": ["Fundraisers", "Corporate Events", "Convention"],
    "arena": ["Corporate Events", "Fundraisers", "Parties", "Convention"],
    "rink": ["Corporate Events", "Fundraisers", "Convention"],
    "skate park": ["Parties"],
    "splash pad": ["Parties"],
    "stadium": ["Corporate Events", "Fundraisers", "Convention"],
    "beach": ["Parties", "Weddings"],
    "marina": ["Parties", "Weddings"],
    "casino": ["Corporate Events", "Parties", "Fundraisers", "Convention"],
    "race track": ["Corporate Events", "Fundraisers", "Convention"],
    "miscellaneous": ["Corporate Events", "Parties", "Fundraisers", "Weddings", "Convention"],
    "sports field": ["Corporate Events", "Fundraisers", "Parties", "Convention"],
    "studio": ["Corporate Events", "Parties", "Seminars", "Weddings", "Convention"]
}



###############################################################
#################### Functions & Classes ######################
###############################################################

class MyProblem(ElementwiseProblem):
    def __init__(self, data):
        super().__init__(n_var=1, n_obj=2, n_constr=0, xl=0, xu=len(data)-1)  # Use row indices as variables
        self.data = data

    def _evaluate(self, x, out, *args, **kwargs):
        # Convert the index (x[0]) to the corresponding row
        idx = int(x[0])  # Ensure x is an integer
        price = self.data.iloc[idx]['Price']
        co2 = self.data.iloc[idx]['CO2']
        out["F"] = [price, co2]

def connect_to_db():
    conn = sqlite3.connect("../database/SeniorProject.db", check_same_thread=False)
    return conn

db_path = '../database/SeniorProject5.db'  # Update the path to match your setup

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

db_path_2 = '../database/SeniorProject3.db'  # Update the path to match your setup

def get_db_connection_2():
    conn = sqlite3.connect(db_path_2)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def optimize_venues(user_province, event_type, user_budget, user_guest):
    conn = connect_to_db()
    print("Database is connect successfully!")
    venue = pd.read_csv('venue.csv')
    print('load venue success', venue.head(10))
    # sort venue columns
    venue = venue[venue['Prov_terr'] == user_province]
    print('match venue with province:', venue.head(10))
    venue = venue[venue['Price'] <= user_budget]
    print('match venue with budget:', venue.head(10))
    venue = venue[venue['Max_audience'] >= user_guest]
    print('match venue with guests:', venue.head(10))
    print(venue.head(10))
    venue2 = venue[venue["ODRSF_facility_type"].isin([facility for facility, events in event_type_mapping.items() if event_type in events])]
    venue2 = venue2[['ID', 'Latitude', 'Longitude', 'Facility_Name', 'Price', 'ODRSF_facility_type']]
    print('match venue with event type:', venue2.head(10))

    # Step 1: Get the list of IDs from venue2
    venue_ids = venue2['ID'].tolist()
    
    # Step 2: Convert the list of IDs to a string for use in the SQL query
    id_string = ', '.join(map(str, venue_ids))  # Convert list of integers to comma-separated string
    
    co2_query = f"""
    SELECT venueID, MAX(Date) AS Date, CO2
    FROM co2
    WHERE venueID IN ({id_string})
    GROUP BY venueID
    ORDER BY venueID
    """
    
    co2 = pd.read_sql_query(co2_query, conn)
    print("load co2 by venueID:",co2.head(10))
    
    merged_data = pd.merge(venue2, co2, left_on='ID', right_on='venueID', how='inner')
    merged_data = merged_data.drop(columns=['venueID'])
    print('merge co2 and venue',merged_data.head(10))
    
    problem = MyProblem(merged_data)  
    algorithm = SPEA2(pop_size=100)
    termination = get_termination("n_gen", 50)
    res = minimize(problem, algorithm, termination, seed=1, save_history=True)

    # Extract indices and objectives
    pareto_indices = res.X[:, 0].astype(int)
    pareto_front = pd.DataFrame(res.F, columns=['Price', 'CO2'])

    pareto_solutions = merged_data.iloc[pareto_indices].reset_index(drop=True)
    
    closest_venues = pd.concat([pareto_solutions, pareto_front], axis=1)

    # Display results
    print("closest_venues:", closest_venues)
    print("closest_venues:", closest_venues.info())
    closest_venues = closest_venues.groupby('ID', as_index=False).first()
    # closest_venues = pd.DataFrame(closest_venues)
    closest_venues['CO2'] = closest_venues['CO2'].round(2)


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
    csv_file_path = os.path.join(CSV_DIR, f'{city}_monthly_avg_co2.csv')

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
        print("Predictions 1: ",predictions)

        # Return predictions for all requested days
        return jsonify({"predictions": predictions})

    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

@app.route('/predict-csv', methods=['POST'])
def predict2():
    try:
        # Get the data from the request
        data = request.get_json()

        # Extract selected city and days to predict
        city_name = data.get('city_name')
        days_to_predict = data.get('days')
        datetime_str = '2023-03' # Actual code: data.get('datetime')
        model_name = data.get('model_name')

        
        print("city_name: ",city_name)
        print("days_to_predict: ",days_to_predict)
        print("datetime_str: ",datetime_str)
        print("model_name: ",model_name)

        # Filter csv file based on daysto predict
        csv_file_path = os.path.join(CSV_DIR_MK, f'{city_name}_{model_name}_{days_to_predict}.csv')
        print("csv_file_path: ",csv_file_path)
        df = pd.read_csv(csv_file_path)

        # Get the last 6 rows and convert to a list of dictionaries
        predictions = df.tail(6).to_dict(orient='records')

        print("Predictions: ",predictions)

        # Return predictions for all requested days
        return jsonify({"predictions": predictions})

    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    
    conn = get_db_connection_2()
    
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
    event_name = data.get('event_name')
    type_of_event = data.get('event_type')
    event_date = data.get('start_date')
    number_of_guests = data.get('guests')
    location_of_province = data.get('province')
    user_budget = data.get('budget')
    user_budget = int(user_budget)
    match = re.search(r'\d+-\d+', number_of_guests)
    if match:
        max_guests = int(match.group(0).split('-')[1])  # Split by '-' and take the second number
    else:
        match_plus = re.search(r'(\d+)\+', number_of_guests)
        if match_plus:
            max_guests = int(match_plus.group(1))  # Extract the number before '+'
        else:
            raise ValueError(f"Invalid guests format: {number_of_guests}")
    number_of_guests = max_guests
    # email = data.get('Email')
    # describe_goals = data.get('Describe-Your-Goals')

    app.logger.info(f"Received event: {event_name}, Type: {type_of_event}, Date: {event_date}, "
                    f"Number of guests: {number_of_guests}, Location: {location_of_province}, "
                    #f"Email: {email}, Goals: {describe_goals}"
                    )
    
    if location_of_province not in city_coordinates:
        return jsonify({"error": "Invalid location"}), 400
    
    # Get latitude and longitude boundaries for the province -- to retrieve distance
    # lat_min = city_coordinates[location_of_province]['lat_min']
    # lat_max = city_coordinates[location_of_province]['lat_max']
    # lon_min = city_coordinates[location_of_province]['lon_min']
    # lon_max = city_coordinates[location_of_province]['lon_max']

    # user_latitude = (lat_min + lat_max) / 2
    # user_longitude = (lon_min + lon_max) / 2
    # user_location = [user_latitude, user_longitude]
    closest_venues = optimize_venues(location_of_province, type_of_event, user_budget, max_guests)
    
    print(closest_venues)

    return jsonify(closest_venues)

@app.route('/venue', methods=['POST'])
def get_venue():
    data = request.get_json()
    print(data)

    # Read the venue.csv file
    venue_data = pd.read_csv('venue.csv')
    venue_id = data.get('ID')
    print(venue_id)
    venue_id = int(venue_id)

    # Filter the data based on the venue_id
    venue = venue_data[venue_data['ID'] == int(venue_id)]

    # Check if the venue exists
    if venue.empty:
        return jsonify({"error": "Venue not found"}), 404

    # Convert the row to a dictionary
    venue_dict = venue.iloc[0].to_dict()

    # Return the venue data as JSON
    return jsonify(venue_dict) 
  
###############################################################
#################### connect to DB ############################
###############################################################
# def connect_to_db():
#     conn = sqlite3.connect('SeniorProject.db')
#     return conn

###############################################################
#################### Login api ################################
###############################################################

app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('Email')
    password = data.get('Password')

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, FirstName, LastName, Email, PhoneNumber FROM user WHERE Email = ? AND Password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        token = jwt.encode({
            "user_id": user[0],
            "exp": datetime.utcnow() + timedelta(hours=2)  # Token 有效期
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user[0],
                "FirstName": user[1],
                "LastName": user[2],
                "Email": user[3],
                "PhoneNumber": user[4]
            }
        })
    else:
        return jsonify({"success": False, "message": "Incorrect Email or Password"}), 401

###############################################################
#################### Profile api ##############################
###############################################################


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"success": False, "message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
        except:
            return jsonify({"success": False, "message": "Token is invalid"}), 401

        return f(user_id, *args, **kwargs)
    return decorated

@app.route('/profile', methods=['GET'])
@token_required
def profile(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT FirstName, LastName, Email, PhoneNumber FROM user WHERE ID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "success": True,
            "user": {
                "FirstName": user[0],
                "LastName": user[1],
                "Email": user[2],
                "PhoneNumber": user[3]
            }
        })
    else:
        return jsonify({"success": False, "message": "User not found"}), 404

###############################################################
#################### Main Port:5000 ###########################
###############################################################
if __name__ == '__main__':
    app.run(debug=True, port=5000)


# CO2 prediction api :(POST) http://127.0.0.1:5000/predict
# Cost location api :(GET) http://127.0.0.1:5000/get_cost_by_location?location=Ontario
# Get user input event form data : (POST) http://127.0.0.1:5000/submit_event
